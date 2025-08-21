@echo off
setlocal enabledelayedexpansion

REM ====== הגדרות ======
set IMAGE=YOUR_DOCKERHUB_USER/hostile-tweets-ex:latest
set NAMESPACE=neria-hostile-ex

echo [*] מעבר לפרויקט %NAMESPACE% (יצור אוטומטי אם לא קיים)
oc new-project %NAMESPACE% 1>nul 2>nul
oc project %NAMESPACE%

echo [*] ניקוי משאבים קודמים
oc delete route hostile-tweets-ex --ignore-not-found
oc delete svc hostile-tweets-ex --ignore-not-found
oc delete deploy hostile-tweets-ex --ignore-not-found
oc delete secret mongo-conn --ignore-not-found
oc delete configmap hostile-config --ignore-not-found

echo [*] יצירת Secret לחיבור Mongo (דוגמא עם הקרדנצלס מהמטלה)
oc create secret generic mongo-conn ^
  --from-literal=MONGO_URI="mongodb+srv://IRGC:iraniraniran@iranmaldb.gurutam.mongodb.net/"

echo [*] יצירת ConfigMap (DB/Collection/Weapons path)
oc apply -f infra\configmap.yaml

echo [*] עדכון אימג' בקובץ ה-Deployment (ודאו ששיניתם את ה-image בקובץ עצמו)
oc apply -f infra\deployment.yaml

echo [*] יצירת Service ו-Route
oc apply -f infra\service.yaml
oc apply -f infra\route.yaml

echo [*] ממתין ל-Deployment להתייצב...
oc rollout status deploy/hostile-tweets-ex

echo [*] שליפת ה-URL של ה-Route:
for /f "delims=" %%i in ('oc get route hostile-tweets-ex -o jsonpath^="{.spec.host}"') do set HOST=%%i
echo URL: https://%HOST%
echo [*] בדיקות לדוגמא (דורש curl):
echo curl https://%HOST%/health
echo curl https://%HOST%/processed

endlocal
