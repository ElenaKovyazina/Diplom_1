import pytest
from unittest.mock import MagicMock
from praktikum.burger import Burger

class TestBurger:

    #Проверка инициализации
    def test_init(self):
        burger = Burger()

        assert burger.bun is None and burger.ingredients == []

    #Проверка работы метода, добавляющего булочку в бургер
    def test_set_buns_correctly(self):
        burger = Burger()
        mock_bun = MagicMock()
        
        burger.set_buns(mock_bun)
        
        assert burger.bun == mock_bun

    #Пооверка добавления нового ингредиента в бургер
    def test_add_ingredient(self):
        burger = Burger()
        mock_ingredient = MagicMock()
        
        burger.add_ingredient(mock_ingredient)
        
        assert mock_ingredient in burger.ingredients
        assert len(burger.ingredients) == 1

    
    #Проверка удаления ингредиента по его индексу
    def test_remove_ingredient(self):
        burger = Burger()
        mock_ingredient = MagicMock()
        burger.add_ingredient(mock_ingredient)
        
        burger.remove_ingredient(0)
        
        assert mock_ingredient not in burger.ingredients
        assert len(burger.ingredients) == 0

    #Проверка изменения порядка следования ингридиентов
    def test_move_ingredient(self):
        burger = Burger()
        mock_ing_1 = MagicMock()
        mock_ing_2 = MagicMock()
        burger.add_ingredient(mock_ing_1)
        burger.add_ingredient(mock_ing_2)
        
        burger.move_ingredient(0, 1)
        
        assert burger.ingredients == [mock_ing_2, mock_ing_1]

    #Проверка работы метода get price, высчитывающего конечную стоимость бургера
    @pytest.mark.parametrize(
        "bun_price, ingredient_prices, expected_total",
        [
            (200.0, [50.0, 20.0], 470.0),             # 2 ингредиента
            (150.0, [], 300.0),                       # 0 ингредиентов (только булка)
            (120.0, [50.0, 0.0], 290.0),              # с бесплатным ингредиентом
            (100.0, [10.0, 20.0, 30.0, 40.0], 300.0), # 4 ингредиента
            (0.0, [25.5], 25.5),                      # дробные числа, 1 ингредиент и бесплатная булка
            (0.0, [0.0], 0.0),                        # всё бесплатно
            (-20.0, [30.0, 50.0], 40.0),              # отрицательная цена булки
            (170.0, [-50.0, 60.0], 350.0)             # отрицательная цена ингредиента

        ]
    )
    def test_get_price(self, bun_price, ingredient_prices, expected_total):
    
        burger = Burger()
        
        mock_bun = MagicMock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        for price in ingredient_prices:
            mock_ingredient = MagicMock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
            

        assert burger.get_price() == pytest.approx(expected_total)


    #Проверка формирования чека

    @pytest.mark.parametrize(
        "bun_name, bun_price, ingredients_data, expected_receipt",
        [
             # 1. Бургер с одним ингредиентом
            (
                "Флюоресцентная булка", 100.0,
                [("sauce", "Spicy-X", 50.0)],
                "(==== Флюоресцентная булка ====)\n"
                "= sauce Spicy-X =\n"
                "(==== Флюоресцентная булка ====)\n\n"
                "Price: 250.0"  # Формула расчета: (100 * 2) + 50 = 250
            ),
            # 2. Бургер вообще без ингредиентов
            (
                "Краторная булка", 120.0,
                [],  # Список ингредиентов пуст
                "(==== Краторная булка ====)\n"
                "(==== Краторная булка ====)\n\n"
                "Price: 240.0"  # 120 * 2 = 240
            ),
            # 3. Бургер со множеством ингредиентов
            (
                "Звездная булка", 100.0,
                [
                    ("sauce", "Чили", 40.0),
                    ("filling", "Котлета", 150.0),
                    ("sauce", "Сырный", 30.0)
                ],
                "(==== Звездная булка ====)\n"
                "= sauce Чили =\n"
                "= filling Котлета =\n"
                "= sauce Сырный =\n"
                "(==== Звездная булка ====)\n\n"
                "Price: 420.0"  
            ),

            
            # 4. Некорректный регистр
            (
                "Булка", 100.0,
                [("FiLLiNg", "Говядина", 80.0), ("SAUCE", "Горчица", 20.0)],
                "(==== Булка ====)\n"
                "= filling Говядина =\n"
                "= sauce Горчица =\n"
                "(==== Булка ====)\n\n"
                "Price: 300.0"
            ),
            # 5. Пустые строки вместо названий 
            (
                "", 0.0,
                [("", "", 0.0)],
                "(====  ====)\n"
                "=   =\n"
                "(====  ====)\n\n"
                "Price: 0.0"
            ),
            # 6. Названия со специальными символами, цифрами и пробелами
            (
                "Супер-Булка №1", 150.0,
                [("SAUCE", "Кисло-Сладкий (v2.0!)", 60.0)],
                "(==== Супер-Булка №1 ====)\n"
                "= sauce Кисло-Сладкий (v2.0!) =\n"
                "(==== Супер-Булка №1 ====)\n\n"
                "Price: 360.0"
            )
        ]
    )
    def test_get_receipt_positive_and_negative_scenarios(
        self, bun_name, bun_price, ingredients_data, expected_receipt
    ):
        
        burger = Burger()
        
        mock_bun = MagicMock()
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)
        
        for ing_type, ing_name, ing_price in ingredients_data:
            mock_ingredient = MagicMock()
            mock_ingredient.get_type.return_value = ing_type
            mock_ingredient.get_name.return_value = ing_name
            mock_ingredient.get_price.return_value = ing_price
            burger.add_ingredient(mock_ingredient)
            
        actual_receipt = burger.get_receipt()
        assert actual_receipt == expected_receipt
