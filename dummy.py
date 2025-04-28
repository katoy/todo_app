import json
# json を詠み込む
def read_json(filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'{filename} not found')
        return None
    except json.JSONDecodeError as e:
        print(f'JSONDecodeError: {e}')
        return None

# 閏年を判定するメソッド
def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


if __name__ == "__main__":
    x =read_json('todos.json')
    print(x)

    # 閏年を判定するメソッドのテスト
    # いくつかの年の配列から閏年だけを取り出す
    years = [
        2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009,
        2100,
        -4, 1600, 1700, 1800, 1900
    ]

    leap_years = [year for year in years if is_leap_year(year)]
    print(leap_years)


