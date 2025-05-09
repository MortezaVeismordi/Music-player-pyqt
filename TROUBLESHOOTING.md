# راهنمای رفع مشکلات نصب

## خطای Microsoft Visual C++ Build Tools

اگر با خطای زیر مواجه شدید:
```
error: Microsoft Visual C++ 14.0 or greater is required
```

### راه حل‌ها:

1. **نصب Visual C++ Build Tools (توصیه شده)**:
   - به [صفحه دانلود Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) بروید
   - فایل نصبی را دانلود و اجرا کنید
   - در زمان نصب، گزینه "Desktop development with C++" را انتخاب کنید
   - پس از نصب، محیط مجازی را حذف کرده و دوباره نصب کنید:
     ```bash
     # حذف محیط مجازی قبلی
     rmdir /s /q venv
     
     # اجرای مجدد اسکریپت نصب
     setup.bat
     ```

2. **استفاده از نسخه‌های از پیش کامپایل شده**:
   - فایل `requirements.txt` را با محتوای زیر جایگزین کنید:
     ```
     PyQt5==5.15.9
     PyQt5-Qt5==5.15.2
     PyQt5-sip==12.12.2 --only-binary :all:
     mutagen==1.46.0
     pygame==2.5.2 --only-binary :all:
     ```
   - سپس محیط مجازی را حذف و دوباره نصب کنید:
     ```bash
     rmdir /s /q venv
     setup.bat
     ```

## خطای نصب Pygame

اگر با خطای زیر مواجه شدید:
```
ModuleNotFoundError: No module named 'distutils.msvccompiler'
```

### راه حل‌ها:

1. **نصب ابزارهای ساخت**:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install setuptools wheel
   ```

2. **استفاده از نسخه از پیش کامپایل شده**:
   - در فایل `requirements.txt` از فلگ `--only-binary :all:` برای pygame استفاده کنید:
     ```
     pygame==2.5.2 --only-binary :all:
     ```

3. **نصب دستی pygame**:
   - به [صفحه دانلود pygame](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) بروید
   - فایل wheel مناسب با نسخه Python خود را دانلود کنید
   - با دستور زیر نصب کنید:
     ```bash
     pip install pygame‑2.5.2‑cp39‑cp39‑win_amd64.whl
     ```
   (نام فایل را با فایلی که دانلود کرده‌اید جایگزین کنید)

## سایر مشکلات رایج

### خطای "pip not found"
اگر با خطای "pip not found" مواجه شدید:
```bash
python -m ensurepip --default-pip
```

### خطای "python not found"
اگر با خطای "python not found" مواجه شدید:
1. مطمئن شوید که Python در PATH سیستم قرار دارد
2. یا از مسیر کامل Python استفاده کنید:
   ```bash
   C:\Path\To\Python\python.exe -m venv venv
   ```

### خطای "Access denied"
اگر با خطای دسترسی مواجه شدید:
1. Command Prompt یا PowerShell را با دسترسی Administrator اجرا کنید
2. یا از مسیر دیگری برای نصب استفاده کنید که دسترسی نوشتن داشته باشید 