import re


def read_input_file(filename):
    with open(filename, 'r', encoding='utf-8') as input_file:

        input_file.readline()

        final_data = []
        elements_pattern = re.compile(r'\,')
        lfs_pattern = re.compile(r'\w+')
        phone_pattern = re.compile(r'(8|\+7)\s?\(?(\s?\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})')
        phone_subst = r'+7(\2)\3-\4-\5'
        phone_pattern_add = re.compile(r'\(?\доб\.?\ ?(\d{4})\)?')
        phone_pattern_add_subst = r'доб.\1'

        for line in input_file:
            split_result = elements_pattern.split(line)
            if split_result[2] == '' and split_result[1] == '':
                lfs = lfs_pattern.findall(split_result[0])
                lastname = lfs[0] if len(lfs) >= 1 else ''
                firstname = lfs[1] if len(lfs) >= 2 else ''
                surname = lfs[2] if len(lfs) >= 3 else ''
            elif split_result[2] == '':
                lfs = lfs_pattern.findall(split_result[1])
                surname = lfs[1] if len(lfs) >= 2 else ''
                firstname = lfs[0] if len(lfs) >= 1 else ''
                lfs = lfs_pattern.findall(split_result[0])
                firstname = lfs[1] if len(lfs) >= 2 else firstname
                lastname = lfs[0] if len(lfs) >= 1 else ''
            else:
                lastname = split_result[0]
                firstname = split_result[1]
                surname = split_result[2]

            phone_main = phone_pattern.sub(phone_subst, split_result[5])
            phone_temp = phone_main[0:16]
            phone_add = phone_pattern_add.sub(phone_pattern_add_subst, phone_main)[17:25]

            if phone_add != '':
                phone = f'{phone_temp} {phone_add}'
            else:
                phone = phone_temp

            final_data.append({'lastname': lastname, 'firstname': firstname, 'surname': surname,
                               'organization': split_result[3], 'position': split_result[4],
                               'phone': phone, 'email': split_result[6]})
        return final_data


def clear_temp_data(data):
    for d in data:
        for k, v in d.items():
            if isinstance(v, str):
                d[k] = v.replace('\n', '')
    return data


def create_output_file(data):
    with open('output_file.csv', 'w', encoding='utf-8') as output_file:
        output_file.write('lastname,firstname,surname,organization,position,phone,email\n')

        unique_data = []
        seen = set()

        for item in data:
            name = f"{item['lastname']} {item['firstname']}"
            if name not in seen:
                seen.add(name)
                unique_data.append(item)
            else:
                for unique_item in unique_data:
                    if unique_item['lastname'] == item['lastname'] and unique_item['firstname'] == item['firstname']:
                        for key, value in item.items():
                            if value and value != unique_item[key]:
                                unique_item[key] += f'{value}'
        for data in unique_data:
            lastname = data['lastname']
            firstname = data['firstname']
            surname = data['surname']
            organization = data['organization']
            position = data['position']
            phone = data['phone']
            email = data['email']
            output_file.write(f'{lastname},{firstname},{surname},{organization},{position},{phone},{email}\n')


if __name__ == '__main__':
    temp_data = read_input_file('input_file.csv')
    data_to_create_output_file = clear_temp_data(temp_data)
    create_output_file(data_to_create_output_file)
