# coding=UTF-8
import pandas as pd
import codecs
import os
import shutil
import json


def copy_file(sourceSrcfile, dsDir):
    if os.path.exists(dsDir) is False:
        os.makedirs(dsDir)
    if os.path.isfile(sourceSrcfile):
        shutil.copy(sourceSrcfile, dsDir)
        print('copy file {}  ==> {}'.format(sourceSrcfile, dsDir))


def copy_files_to_dir(sourceSrcfiles, dsDir):
    for file in sourceSrcfiles:
        copy_file(file, dsDir)


def read_excel_to_template(source_file, target_file, intent_type):
    excel_file = pd.read_excel(source_file, sheet_name=intent_type)

    op = excel_file.动作
    entity = excel_file.实体
    domain = excel_file.domain
    intent = excel_file.意图
    hard_code = excel_file.hard_code

    with codecs.open(target_file, 'w', encoding='utf-8') as f:
        for o, e, d, i, h in zip(op, entity, domain, intent, hard_code):
            if pd.isna(h):
                h = 0
            if not pd.isna(o) and not pd.isna(e):
                print(o + e, d, i, int(h), file=f, sep=',', end='\r\n')
                print(e + o, d, i, int(h), file=f, sep=',', end='\r\n')
            elif pd.isna(o) and not pd.isna(e):
                print(e, d, i, int(h), file=f, sep=',', end='\r\n')
            # skip blank line
            elif pd.isna(o) and pd.isna(e) and pd.isna(d) and pd.isna(i):
                pass
            else:
                raise ValueError('Invalid data format')


def read_excel_to_entity(source_file: str, target_file: str, sheet_name='实体词') -> None:
    excel_file = pd.read_excel(source_file, sheet_name=sheet_name)

    entity = excel_file.实体词

    with codecs.open(target_file, 'w', encoding='utf-8') as f:
        for e in entity:
            if not pd.isna(e):
                print(e, file=f, sep='', end='\r\n')
            # skip blank line
            elif pd.isna(e):
                pass
            else:
                raise ValueError('Invalid data format')


def read_excel_to_op(source_file: str, target_file: str, sheet_name='动作词') -> None:
    excel_file = pd.read_excel(source_file, sheet_name=sheet_name)

    op = excel_file.动作词

    with codecs.open(target_file, 'w', encoding='utf-8') as f:
        for o in op:
            if not pd.isna(o):
                print(o, file=f, sep='', end='\r\n')
            # skip blank line
            elif pd.isna(o):
                pass
            else:
                raise ValueError('Invalid data format')


def save_json_file(json_string, file):
    with codecs.open(file, 'w', 'utf-8') as _out:
        _out.write(json.dumps(json_string, ensure_ascii=False, indent=2))
        _out.flush()
        _out.close()


if __name__ == '__main__':
    BASE_DIR = '../../../'

    read_excel_to_template(BASE_DIR + 'model/excel_to_config/excel_data/symp_rule.xlsx',
                           BASE_DIR + 'model/excel_to_config/excel_data/symp_template.list',
                           intent_type='意图说法表')
    read_excel_to_entity(BASE_DIR + 'model/excel_to_config/excel_data/symp_rule.xlsx',
                         BASE_DIR + 'model/excel_to_config/excel_data/entity.txt',
                         sheet_name='实体词')
    read_excel_to_op(BASE_DIR + 'model/excel_to_config/excel_data/symp_rule.xlsx',
                     BASE_DIR + 'model/excel_to_config/excel_data/op.txt',
                     sheet_name='动作词')
    dsDir = BASE_DIR + 'model/rules/'
    sourceSrcfiles = [BASE_DIR + 'model/excel_to_config/excel_data/symp_template.list',
                      ]
    copy_files_to_dir(sourceSrcfiles, dsDir)


    dsDir = BASE_DIR + 'model/symptom/'
    sourceSrcfiles = [BASE_DIR + 'model/excel_to_config/excel_data/op.txt',
                      BASE_DIR + 'model/excel_to_config/excel_data/entity.txt'
                      ]
    copy_files_to_dir(sourceSrcfiles, dsDir)