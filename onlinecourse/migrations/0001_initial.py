# Django 4.2.3 によって 2025-03-23 06:25 に生成されたマイグレーションファイル

from django.conf import settings  # Django の設定情報をインポート
from django.db import migrations, models  # マイグレーションとデータモデルのモジュールをインポート
import django.db.models.deletion  # 関連するオブジェクト削除の挙動を定義
import django.utils.timezone  # タイムゾーン対応の日時操作モジュール

class Migration(migrations.Migration):

    initial = True  # 初回のマイグレーションを示すフラグ

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),  # ユーザーモデルとの依存関係
    ]

    operations = [
        # Course モデルの作成
        migrations.CreateModel(
            name='Course',  # モデル名
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # 主キー ID
                ('name', models.CharField(default='online course', max_length=30)),  # コース名 (デフォルトは "online course")
                ('image', models.ImageField(upload_to='course_images/')),  # コース画像のアップロード先を指定
                ('description', models.CharField(max_length=1000)),  # コースの説明 (最大 1000 文字)
                ('pub_date', models.DateField(null=True)),  # 公開日 (null 許可)
                ('total_enrollment', models.IntegerField(default=0)),  # 登録者数 (デフォルト 0)
            ],
        ),
        # Lesson モデルの作成
        migrations.CreateModel(
            name='Lesson',  # モデル名
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # 主キー ID
                ('title', models.CharField(default='title', max_length=200)),  # レッスンタイトル (デフォルト "title")
                ('order', models.IntegerField(default=0)),  # レッスンの順番 (デフォルト 0)
                ('content', models.TextField()),  # レッスンの内容
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.course')),  # Course との外部キー (コースが削除されると関連レッスンも削除)
            ],
        ),
        # Learner モデルの作成
        migrations.CreateModel(
            name='Learner',  # モデル名
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # 主キー ID
                ('occupation', models.CharField(  # 職業
                    choices=[('student', 'Student'), ('developer', 'Developer'),
                             ('data_scientist', 'Data Scientist'), ('dba', 'Database Admin')],
                    default='student', max_length=20)),  # 選択肢を定義 (デフォルトは "student")
                ('social_link', models.URLField()),  # SNS リンク
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # ユーザーとの外部キー
            ],
        ),
        # Instructor モデルの作成
        migrations.CreateModel(
            name='Instructor',  # モデル名
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # 主キー ID
                ('full_time', models.BooleanField(default=True)),  # フルタイム講師かどうか (デフォルト True)
                ('total_learners', models.IntegerField()),  # 受講生の総数
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # ユーザーとの外部キー
            ],
        ),
        # Enrollment モデルの作成 (受講情報)
        migrations.CreateModel(
            name='Enrollment',  # モデル名
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # 主キー ID
                ('date_enrolled', models.DateField(default=django.utils.timezone.now)),  # 受講開始日 (デフォルトで現在時刻)
                ('mode', models.CharField(  # 受講モード
                    choices=[('audit', 'Audit'), ('honor', 'Honor'), ('BETA', 'BETA')],
                    default='audit', max_length=5)),  # 選択肢を定義 (デフォルトは "audit")
                ('rating', models.FloatField(default=5.0)),  # 受講評価 (デフォルト 5.0)
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.course')),  # Course との外部キー
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),  # ユーザーとの外部キー
            ],
        ),
        # Course モデルに instructors フィールドを追加 (Instructor との多対多関係)
        migrations.AddField(
            model_name='course',  # 対象モデル
            name='instructors',  # フィールド名
            field=models.ManyToManyField(to='onlinecourse.instructor'),  # Instructor との多対多リレーション
        ),
        # Course モデルに users フィールドを追加 (Enrollment を介したユーザーとの多対多関係)
        migrations.AddField(
            model_name='course',  # 対象モデル
            name='users',  # フィールド名
            field=models.ManyToManyField(through='onlinecourse.Enrollment', to=settings.AUTH_USER_MODEL),  # Enrollment を通じた ManyToMany 関係
        ),
    ]
