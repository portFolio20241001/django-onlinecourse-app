# Django 4.2.3 によって 2025-03-23 06:29 に自動生成されたマイグレーションファイル

from django.db import migrations, models  # Djangoのマイグレーションとデータベースモデル用のモジュールをインポート

class Migration(migrations.Migration):  # マイグレーションクラスの定義

    dependencies = [
        ('onlinecourse', '0001_initial'),  # 依存するマイグレーションファイル（最初のマイグレーション）を指定
    ]

    operations = [
        # Courseモデルのidフィールドの型をBigAutoFieldに変更（より大きなID範囲をサポート）
        migrations.AlterField(
            model_name='course',  # モデル名: Course
            name='id',  # フィールド名: id
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),

        # Enrollmentモデルのidフィールドの型をBigAutoFieldに変更
        migrations.AlterField(
            model_name='enrollment',  # モデル名: Enrollment
            name='id',  # フィールド名: id
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),

        # Instructorモデルのidフィールドの型をBigAutoFieldに変更
        migrations.AlterField(
            model_name='instructor',  # モデル名: Instructor
            name='id',  # フィールド名: id
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),

        # Learnerモデルのidフィールドの型をBigAutoFieldに変更
        migrations.AlterField(
            model_name='learner',  # モデル名: Learner
            name='id',  # フィールド名: id
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),

        # Lessonモデルのidフィールドの型をBigAutoFieldに変更
        migrations.AlterField(
            model_name='lesson',  # モデル名: Lesson
            name='id',  # フィールド名: id
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
