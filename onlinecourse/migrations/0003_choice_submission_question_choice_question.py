# Django 4.2.3 によって 2025-03-23 07:53 に自動生成されたマイグレーションファイル

from django.db import migrations, models  # Djangoのマイグレーションとデータベースモデル用のモジュールをインポート
import django.db.models.deletion  # 外部キーの削除オプションを利用するためのモジュールをインポート

class Migration(migrations.Migration):  # マイグレーションクラスの定義

    dependencies = [
        # 依存するマイグレーション（前のマイグレーションファイル）を指定
        ('onlinecourse', '0002_alter_course_id_alter_enrollment_id_and_more'),
    ]

    operations = [
        # Choice（選択肢）モデルの作成
        migrations.CreateModel(
            name='Choice',  # モデル名: Choice（選択肢）
            fields=[
                # ID フィールド（自動生成される主キー）
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # content フィールド（選択肢の内容）
                ('content', models.CharField(max_length=200)),  # 最大200文字のテキストを保存
                # is_correct フィールド（正解かどうかのフラグ）
                ('is_correct', models.BooleanField(default=False)),  # デフォルトはFalse（不正解）
            ],
        ),

        # Submission（回答提出）モデルの作成
        migrations.CreateModel(
            name='Submission',  # モデル名: Submission（提出）
            fields=[
                # ID フィールド（自動生成される主キー）
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # choices フィールド（複数の選択肢を関連付ける多対多関係）
                ('choices', models.ManyToManyField(to='onlinecourse.choice')),  # Choiceモデルへの多対多関係
                # enrollment フィールド（どの受講者の提出かを示す外部キー）
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.enrollment')),
                # Enrollmentモデルと外部キーで紐付け（受講者の登録情報に関連）
            ],
        ),

        # Question（質問）モデルの作成
        migrations.CreateModel(
            name='Question',  # モデル名: Question（質問）
            fields=[
                # ID フィールド（自動生成される主キー）
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # content フィールド（質問内容）
                ('content', models.CharField(max_length=200)),  # 最大200文字のテキストを保存
                # grade フィールド（質問の配点）
                ('grade', models.IntegerField(default=50)),  # デフォルトで50点
                # course フィールド（どのコースの質問かを示す外部キー）
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.course')),
                # Courseモデルと外部キーで紐付け（質問がどのコースに属するか）
            ],
        ),

        # ChoiceモデルにQuestionモデルとの外部キーを追加
        migrations.AddField(
            model_name='choice',  # 対象モデル: Choice
            name='question',  # フィールド名: question（この選択肢がどの質問に属するか）
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlinecourse.question'),
            # Questionモデルと外部キーで紐付け（選択肢がどの質問に関連するか）
        ),
    ]
