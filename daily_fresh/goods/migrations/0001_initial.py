# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='商品SPU名称', max_length=20)),
                ('detail', tinymce.models.HTMLField(verbose_name='商品详情', blank=True)),
            ],
            options={
                'db_table': 'goods',
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('image', models.ImageField(upload_to='goods', verbose_name='图片路径')),
            ],
            options={
                'db_table': 'goods_image',
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='商品名称', max_length=20)),
                ('desc', models.CharField(verbose_name='商品简介', max_length=256)),
                ('price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('unite', models.CharField(verbose_name='商品单位', max_length=20)),
                ('image', models.ImageField(upload_to='goods', verbose_name='商品图片')),
                ('stock', models.IntegerField(verbose_name='商品库存', default=1)),
                ('sales', models.IntegerField(verbose_name='商品销量', default=0)),
                ('status', models.SmallIntegerField(choices=[(0, '下线'), (1, '上线')], verbose_name='商品状态', default=1)),
                ('goods', models.ForeignKey(verbose_name='商品SPU', to='goods.Goods')),
            ],
            options={
                'db_table': 'goods_sku',
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
            },
        ),
        migrations.CreateModel(
            name='GoodType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('name', models.CharField(verbose_name='种类名称', max_length=20)),
                ('logo', models.CharField(verbose_name='标识', max_length=20)),
                ('image', models.ImageField(upload_to='type', verbose_name='商品类型图片')),
            ],
            options={
                'db_table': 'goods_type',
                'verbose_name': '商品种类',
                'verbose_name_plural': '商品种类',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(verbose_name='商品种类', to='goods.GoodType'),
        ),
        migrations.AddField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(verbose_name='商品', to='goods.GoodsSKU'),
        ),
    ]
