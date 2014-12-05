from api.models import Category

f = open('categories_name.txt','r')
cats = [c.replace("\n", "") for c in f.readlines()]
f.close()

for c in cats:
    new_cat, is_created = Category.objects.get_or_create(name=c)
    if is_created:
        new_cat.save()

