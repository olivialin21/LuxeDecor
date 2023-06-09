# Generated by Django 4.2.1 on 2023-06-07 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0004_product_sub_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="sub_category",
            field=models.ForeignKey(
                limit_choices_to=models.Q(("category", models.F("category"))),
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="web.subcategory",
            ),
        ),
    ]