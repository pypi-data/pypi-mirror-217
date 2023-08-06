# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any

import pydantic
import yaml
from headless.ext.foxway import FoxwayClient
from headless.ext.foxway.v1 import PricelistProduct

from molano.lib.sheets import Spreadsheet
from molano.lib.sheets import SpreadsheetModel


FEATURE_MAPPING: dict[str, str] = {
    'Appearance'            : 'quality.grade.apparent',
    'Battery status'        : 'electronic.battery.health',
    'Brand'                 : 'marketing.brand',
    'Boxed'                 : 'quality.packaging.state',
    'Functionality'         : 'quality.functional.state',
    'Color'                 : 'appearance.color',
    'Cloud Lock'            : 'network.locked',
    'CPU desktops'          : 'computer.cpu',
    'CPU Laptops'           : 'computer.cpu.integrated',
    'GPU desktops'          : 'computer.gpu',
    'GPU laptops'           : 'computer.gpu.integrated',
    'COA'                   : 'computer.os.coa',
    'Drive'                 : 'computer.storage',
    'Keyboard'              : 'computer.keyboard.layout',
    'RAM'                   : 'computer.ram',
    'LCD Graphics array'    : 'computer.display.resolution',
    'Additional Info'       : 'product.remarks.additional',
    'Form factor'           : 'xx'
}

FEATURE_VALUES: dict[str, dict[str, str]] = {
    'molano.nl/grade': {
        'Grade A+'  : 'A+',
        'Grade A'   : 'A',
        'Grade B+'  : 'B+',
        'Grade B'   : 'B',
        'Grade C+'  : 'C+',
        'Grade C'   : 'C',
    }
}


class Item(SpreadsheetModel):
    sku: str
    product_name: str
    available: str
    price: float
    grade: str = pydantic.Field(..., alias='quality.grade.apparent')
    keyboard: str = pydantic.Field('', alias='computer.keyboard.layout')
    ram: str = pydantic.Field('', alias='computer.ram')
    storage: str = pydantic.Field('', alias='computer.storage')
    color: str = pydantic.Field('', alias='appearance.color')
    remarks: str = pydantic.Field('', alias='product.remarks.additional')



def get_feature_value(key: str, value: str) -> str:
    try:
        return FEATURE_VALUES[key][value]
    except KeyError:
        return value


async def main():
    sheet = Spreadsheet(
        model=Item,
        id='12fZ4JCiPyBwerZULjXZB40ecgAaHDy-HE_y19nrJLaM',
        sheet_id=53925588,
        range='Foxway'
    )
    sheet.clear()
    rows: list[Item] = []
    async with FoxwayClient() as client:
        products: list[Any] = []
        ignored_dimensions: set[str] = {
            'Battery cycles',
            'High Cycle Count',
            'Functionality'
        }
        ignored_battery: set[str] = {
            'physical battery issue (damaged/swollen)',
            'Untested',
            'Worn Battery',
            'Missing Battery',
        }
        ignored_drive: set[str] = {
            'faulty drive',
            'missing drive'
        }

        ignored_packaging: set[str] = {
            'Damaged Box',
            'Incomplete Box'
        }
        for d, i in [('1', '1'), ('11', '12')]:
            query: dict[str, str] = {
                'dimensionGroupId': d,
                'itemGroupId': i,
                'vatMargin': 'false'
            }
            async for dto in client.listall(PricelistProduct, 'working', params=query):
                must_continue = False
                for dimension in dto.dimension:
                    if dimension.key == 'Boxed' and dimension.value in ignored_packaging:
                        must_continue = True
                    if dimension.key == 'Drive' and dimension.value in ignored_drive:
                        must_continue = True
                    if dimension.key == 'PC Fault Descriptions':
                        #print(f"- Skipping item with fault: {dimension.value}")
                        must_continue = True
                    if dimension.key == 'PC Additional Fault':
                        #print(f"- Skipping item with fault: {dimension.value}")
                        must_continue = True
                    if dimension.key == 'Battery status' and dimension.value in ignored_battery:
                        #print(f"- Skipping item with unacceptable battery status: {dimension.value}")
                        must_continue = True
                    if dimension.key == 'Functionality' and dimension.value != 'Working':
                        #print(f"- Skipping item with unacceptable functional state: {dimension.value}")
                        must_continue = True
                    if dimension.key == 'Keyboard' and dimension.value in {'SCA', 'CHE', 'DEU', 'SWE/FIN', 'DNK', 'SVK', 'CZE', 'Missing Keyboard', 'ARABIC', 'KOR', 'RUS', 'NOR'}:
                        must_continue = True
                    if dimension.value == 'Not tested':
                        must_continue = True
                    if dimension.key == 'Cloud Lock' and dimension.value != 'CloudOFF':
                        must_continue = True
                    if dimension.key == 'Additional Info' and dimension.value in {'Brand New Battery', 'Broken seal', 'True Tone Missing', 'Reduced Battery Performance', 'Engraving', 'Heavy cosmetic wear', 'AS-IS'}:
                        # Exclude products with non-original batteries or that have been modified, customized, or
                        # have issues otherwise.
                        must_continue = True

                if must_continue:
                    continue
                product: dict[str, str | float] = {
                    'product_name': dto.product_name,
                    'sku': dto.sku,
                    'price': dto.price,
                    'available': dto.quantity
                }
                product.update({
                    FEATURE_MAPPING[dimension.key]: get_feature_value(FEATURE_MAPPING[dimension.key], dimension.value)
                    for dimension in dto.dimension if dimension.key not in {'Battery cycles'}
                })
                products.append(product)
                if i == '1':
                    if not str.startswith(product['product_name'], 'Apple') and not str.startswith(product['product_name'], 'Samsung'):
                        continue
                rows.append(Item.parse_obj(product))
    sheet.extend(rows)

if __name__ == '__main__':
    asyncio.run(main())