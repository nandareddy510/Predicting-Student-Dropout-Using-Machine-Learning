from django.shortcuts import render 
from django.contrib import messages 
from app.models import Univesity 
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.neural_network import MLPClassifier 
from sklearn.ensemble import StackingClassifier, RandomForestClassifier, AdaBoostClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import accuracy_score
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        print(name, email, password, confirm_password, contact, address) 
        if password == confirm_password:
            if Univesity.objects.filter(email=email).exists():
                messages.error(request, f"This Email Id Already Exists, Try another")
                return render(request, 'register.html')
            else: 
                queryset = Univesity(name=name, email=email, password=password, contact=contact, address=address)
                queryset.save()
                messages.success(request, f"User Registered Completed Successfully, Thank You")
                return render(request, 'login.html')
        else: 
            messages.error(request, f"Password and Confirm Password does not matched, Try Again")
            return render(request, 'register.html')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Univesity.objects.filter(email=email).first()

        if user:
            if user.password == password:
                messages.success(request, f"User Login Successfully")
                return render(request, 'home.html')
            else: 
                messages.error(request, f"Invalid Password, Try Again")
                return render(request, 'login.html')
        else:
            messages.error(request, f"This Email ID does not exist, Please Register") 
            return render(request, 'login.html')
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def view_dataset(request):
    df = pd.read_csv('app/final_dataset.csv')
    col = df.head(100).to_html()
    return render(request, 'view_dataset.html', {'table':col}) 

df = pd.read_csv('app/final_dataset.csv') 
x = df.drop('Class', axis=1)
y = df['Class']
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)

def model_train(request):
    if request.method == 'POST':
        algo = request.POST.get('algo')
        print(algo)
        if algo == '1':
            mlp = MLPClassifier()
            mlp.fit(x_train, y_train)
            pred = mlp.predict(x_train)
            accuracy = accuracy_score(y_train, pred)
            msg = f"Accuracy Score of MLP: {accuracy}"
            return render(request, 'model_train.html', {'msg':msg})
        elif algo == '2':
            ad = AdaBoostClassifier()
            ad.fit(x_train, y_train)
            pred = ad.predict(x_train)
            accuracy = accuracy_score(y_train, pred)
            msg = f"Accuracy Score of Adaboost: {accuracy}"
            return render(request, 'model_train.html', {'msg':msg})
        elif algo == '3':
            base_model = [
                ('rf', RandomForestClassifier()),
                ('dt', DecisionTreeClassifier())
            ] 

            meta_model = LogisticRegression()

            stc = StackingClassifier(estimators = base_model, final_estimator=meta_model)
            stc.fit(x_train, y_train)
            pred = stc.predict(x_train)
            accuracy = accuracy_score(y_train, pred)
            msg = f"Accuracy Score of Stacking Classifier : {accuracy}"
            return render(request, 'model_train.html', {'msg':msg}) 
        elif algo == '4':
            log_clf = LogisticRegression(max_iter=200)
            rf_clf = RandomForestClassifier(n_estimators=100)
            dt_clf = DecisionTreeClassifier()
            vtc = VotingClassifier(estimators=[('lr', log_clf), ('rf', rf_clf), ('dt', dt_clf)],
                                        voting='hard') 
            vtc.fit(x_train, y_train)
            pred = vtc.predict(x_train)
            accuracy = accuracy_score(y_train, pred)
            msg = f"Accuracy Score of Voting Classifier : {accuracy}"
            return render(request, 'model_train.html', {'msg':msg})

    return render(request, 'model_train.html')

def prediction(request):
    if request.method == 'POST':
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')
        num3 = request.POST.get('num3')
        num4 = request.POST.get('num4')
        num5 = request.POST.get('num5')
        num6 = request.POST.get('num6')
        num7 = request.POST.get('num7')
        num8 = request.POST.get('num8')
        num9 = request.POST.get('num9')
        num10 = request.POST.get('num10')
        num11 = request.POST.get('num11')
        num12 = request.POST.get('num12')
        num13 = request.POST.get('num13')
        num14 = request.POST.get('num14')
        num15 = request.POST.get('num15')
         

        input = [[num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15]] 
        base_model = [
                ('rf', RandomForestClassifier()),
                ('dt', DecisionTreeClassifier())
            ]
        meta_model = LogisticRegression()
        stc = StackingClassifier(estimators = base_model, final_estimator=meta_model)
        stc.fit(x_train, y_train)
        result = stc.predict(input) 
        if result == 0:
            msg = "Prediction of University student is Dropout"
        elif result == 1:
            msg = "Prediction of University student is Enrolled"
        elif result == 2:
            msg = "Prediction of University student is Graduated" 
        
        return render(request, 'prediction.html', {'msg':msg})


    return render(request, 'prediction.html')   