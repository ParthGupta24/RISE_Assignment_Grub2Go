import streamlit as st
import datetime

with open("Menu_Card.json", 'r') as fr:
    cuisines = eval(fr.read())

gst = 5

st.set_page_config(page_title='Demo App', layout='centered')

st.title('Grub 2 Go')

user_panel = st.sidebar
form = user_panel.form(key = "Food Form")
name = form.text_input("Name : ", key='name')
age = form.number_input("Age : ", key='age', min_value=0, value=18)
dob = form.date_input("Date of Birth : ", value='today', min_value=datetime.date(year=1970, month=1, day=1))
city = form.text_input("City", key='city')

def validate():
    if not name:
        form.error("Please enter your name")
submit = form.form_submit_button("Submit", on_click=validate)

menu = st.expander('Menu Card')
categories = user_panel.expander("Select your favourite cuisines")
all = categories.checkbox("All", key='all')

if all:
    cuisine_labels = dict()
    for i in cuisines.keys():
        cuisine_labels.update({i:categories.checkbox(str(i).capitalize(), value=True)})
else:
    cuisine_labels = dict()
    for i in cuisines.keys():
        cuisine_labels.update({i:categories.checkbox(str(i).capitalize())})

class item:
    def __init__(self, menu, item_name, price, menu_name):
        self.menu = menu
        self.col1, self.col2, self.col3 = menu.columns(3)
        self.item = item_name
        self.price = price
        self.col1.write(str(item_name))
        self.col2.write("Rs "+str(price))
        self.qty = self.col3.number_input("Qty", min_value=0, value=0, key=str(menu_name) + str(item_name))
class Menu:
    def __init__(self, cuisine, items, cuisine_name):
        self.cuisine = cuisine
        self.items = [item(cuisine, key, value, cuisine_name) for key, value in items.items()]
        self.total = 0
        for i in self.items:
            self.total += i.price * i.qty
        self.cuisine.write(f"Sub total : Rs {self.total}")

total = 0
menu_card = dict()
for i in cuisine_labels.keys():
    if cuisine_labels[i]:
        csn = menu.expander(str(i).capitalize()+' Cuisine')
        catalog = Menu(csn, cuisines[i], str(i).capitalize())
        total += catalog.total
        menu_card.update({i:{'csn':csn, 'catalog':catalog}})

if total != 0:
    bill = st.expander("Billing - Order summary:")
    for i in cuisine_labels.keys():
        if cuisine_labels[i]:
            for j in menu_card[i]['catalog'].items:
                if j.qty == 0:
                    continue
                bill.write(f"{j.item} x {j.qty} {'_'*30} : Rs {j.price*j.qty}")
    bill.markdown("------------")
    bill.write(f"Subtotal {'_'*30} : Rs {total}")
    bill.write(f"GST  ({gst}%) {'_'*30} : Rs {total*gst/100}")
    bill.markdown("------------")
    total += total*gst/100
    bill.write(f"Total = Rs {total}")

st.text_area("Please share your feedback:", height=300)

    