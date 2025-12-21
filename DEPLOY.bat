@echo off
set PATH=%PATH%;C:\Users\USER\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin
cd /d C:\Users\USER\Desktop\Enercon-RAG
echo.
echo ====================================
echo  Enercon RAG - Google Cloud Deploy
echo ====================================
echo.
echo Checking gcloud...
gcloud --version
echo.
echo Ready! Now run:
echo   gcloud run deploy enercon-rag --source . --region europe-west1 --allow-unauthenticated
echo.
cmd /k
