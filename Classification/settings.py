IMG_SIZE = 50
image_weight = 50
image_height = 50
image_depth = 3

PATH_DIR = "images/Dataset"
PATH_TRAIN = "Training"
PATH_TEST = "Test"

model_name = "conv64-64x2dense-32dense-Sigmoid"

signs_name_blue = {
    0: "parking",
    1: "zakaz postoju",
	2: "zakaz zatrzymywania sie",
    3: "przejscie dla pieszych",
    4: "droga rowerowa",
    5: "rondo",
	6: "nakaz jazdy z prawej strony znaku",
    7: "nakaz jazdy z lewej strony znaku",
	8: "nakaz jazdy prosto",
	9: "nakaz jazdy prosto lub w prawo",
    10: "nakaz jazdy prosto lub w lewo",
    11: "nakaz skretu w prawo",
    12: "nakaz skretu w lewo",
	13: "droga jednokierunkowa"
}

signs_name_red = {
    0: "zakaz skretu w prawo lub lewo",
    1: "zakaz skretu w lewo",
	2: "ograniczenie 20",
    3: "ograniczenie 30",
	4: "ograniczenie 40",
    5: "ograniczenie 50",
    6: "ograniczenie 60",
    7: "ograniczenie 70",
    8: "ograniczenie 80",
    9: "zakaz wyprzedzania",
    10: "zakaz wjazdu",
    11: "zakaz ruchu",
    12: "STOP",
    13: "zakaz postoju",
    14: "zakaz zatrzymywania sie",
    15: "zakaz jazdy prosto",
    16: "zakaz skretu w prawo"
}

signs_name_yellow = {
    0: "ustap pierwszenstwa",
    1: "pierwszenstwo przejazdu"
}

signs_name = {
    0: "inne",
    1: "pierwszenstwo przejazdu",
	2: "ustap pierwszenstwa",
    3: "ograniczenie 30",
	4: "ograniczenie 40",
    5: "ograniczenie 50",
    6: "ograniczenie 60",
    7: "ograniczenie 70",
    8: "ograniczenie 80",
    9: "zakaz wyprzedzania",
    10: "zakaz wjazdu",
    11: "zakaz ruchu",
    12: "STOP",
    13: "zakaz postoju",
    14: "zakaz zatrzymywania sie",
    15: "przejscie dla pieszych",
    16: "droga rowerowa",
    17: "rondo",
	18: "nakaz jazdy z prawej strony znaku",
    19: "nakaz jazdy z lewej strony znaku",
	20: "nakaz jazdy prosto",
	21: "nakaz jazdy prosto lub w prawo",
    22: "nakaz jazdy prosto lub w lewo",
    23: "nakaz skretu w prawo",
    24: "nakaz skretu w lewo",
	25: "droga jednokierunkowa",
	26: "zakaz jazdy prosto",
	27: "zakaz skretu w prawo",
	28: "zakaz skretu w lewo",
	29: "zakaz skretu w prawo lub lewo",
}

COUNT_OF_CLASSES_BLUE = len(signs_name_blue)
COUNT_OF_CLASSES_RED = len(signs_name_red)
COUNT_OF_CLASSES_YELLOW = len(signs_name_yellow)

