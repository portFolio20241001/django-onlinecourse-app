"""
Django の設定ファイル (settings.py)
このファイルは、Django プロジェクト "myproject" の設定を定義する。
"""

import os  # OS 操作用の標準ライブラリをインポート

# プロジェクトのベースディレクトリを設定
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# すぐに使える開発用設定 - 本番環境には適していない
# 詳細: https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# セキュリティ警告: 本番環境では Secret Key を厳重に管理すること
SECRET_KEY = 'aay0j_9b&ky3a7(8m8il+-1ud(scw12@w5!+5-=gsk6ynzi0ls'

# セキュリティ警告: 本番環境では DEBUG を False にすること
DEBUG = True  # デバッグモードを有効化 (開発用)

# 許可するホスト名を設定 (本番環境では適切に設定すること)
ALLOWED_HOSTS = []

# CSRF（クロスサイトリクエストフォージェリ）保護の信頼できるオリジン
CSRF_TRUSTED_ORIGINS = ['https://*.cognitiveclass.ai']

# アプリケーション定義
INSTALLED_APPS = [
    'onlinecourse.apps.OnlinecourseConfig',  # カスタムアプリ "onlinecourse" を追加
    'django.contrib.admin',  # Django 管理サイト
    'django.contrib.auth',  # 認証システム
    'django.contrib.contenttypes',  # コンテンツタイプフレームワーク
    'django.contrib.sessions',  # セッション管理
    'django.contrib.messages',  # メッセージフレームワーク
    'django.contrib.staticfiles',  # 静的ファイル管理
    'django_extensions',  # ER図作成に必要（石川追加）
]

# ミドルウェア設定
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # セキュリティ関連のミドルウェア
    'django.contrib.sessions.middleware.SessionMiddleware',  # セッション管理
    'django.middleware.common.CommonMiddleware',  # 一般的な HTTP リクエスト処理
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF 保護
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 認証管理
    'django.contrib.messages.middleware.MessageMiddleware',  # メッセージ管理
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # クリックジャッキング対策
]

# ルート URL 設定 (プロジェクトの URL 設定ファイル)
ROOT_URLCONF = 'myproject.urls'

# テンプレートエンジン設定
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Django のテンプレートエンジンを使用
        'DIRS': [],  # テンプレートディレクトリ (必要なら指定)
        'APP_DIRS': True,  # 各アプリ内の `templates` ディレクトリを使用
        'OPTIONS': {
            'context_processors': [  # テンプレートで利用できるコンテキストプロセッサ
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI アプリケーション設定 (Django の WSGI アプリ)
WSGI_APPLICATION = 'myproject.wsgi.application'

# データベース設定
# 詳細: https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite をデータベースエンジンとして使用
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # データベースファイルの保存場所
    }
}

# パスワードバリデーション設定
# 詳細: https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # ユーザー情報との類似性チェック
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # 最小文字数制限
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # よく使われるパスワードの拒否
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # 数字のみのパスワードの拒否
]

# 国際化 (i18n) 設定
# 詳細: https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'  # 言語コード (英語 - 米国)
TIME_ZONE = 'UTC'  # タイムゾーン (協定世界時)
USE_I18N = True  # 国際化 (多言語対応) を有効化
USE_L10N = True  # ローカライズ (日付/数値の書式設定) を有効化
USE_TZ = True  # タイムゾーン対応を有効化

# 静的ファイル (CSS, JavaScript, 画像) の設定
# 詳細: https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'  # 静的ファイルの URL パス
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 静的ファイルの保存先
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')  # メディアファイルの保存先
MEDIA_URL = '/media/'  # メディアファイルの URL パス

# デフォルトのプライマリキーのフィールド設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Django 3.2 以降の推奨設定
