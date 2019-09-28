from django import forms
from ordersapp.models import Order, OrderItem
from mainapp.models import Products


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # вместо разрешенных полей, прописываем кортежи с полями, которые необходимо исключить из форм
        exclude = ('user',)  # Не забывайте ставить запятую, даже если одно значение в кортеже

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    # Добавляем поле «price» к форме элемента заказа
    # Так как это поле не должно сохраняться в базу и проходить валидацию - задаем аргумент required=False
    price = forms.CharField(label='Цена за единицу', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['product'].queryset = Products.get_items()
