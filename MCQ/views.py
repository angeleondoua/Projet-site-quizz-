from django.http import HttpResponse, HttpResponseRedirect
from polls import models

def index(request):
    html_header = "<html><body>"
    html_footer = "</body></html>"
    html_response = ""
    nb_question=1
    Questions = models.listquizz_mcq(nb_question)
    for i in range(nb_question):
        html_question = ""
        Taille = len(Questions[i][1])
        Index = Questions[i][2]
        html_question = html_question + "<fieldset>"
        html_question = html_question + "<legend>" + str(Questions[i][0]) + "</legend>"
        html_question = html_question + "<form method='get' action='take_quiz/'>"
        html_question = html_question + "<p>"
        for j in range(Taille):
            html_question = html_question + f"<input type='checkbox' name={'user_answer'+str(j)} value='{[j+1,Index]}' >"
            html_question = html_question + "<label for='coding'>" + str(Questions[i][1][j]) + "</label>"
            html_question = html_question + "</p>"


        html_response = html_response + html_question
        html_response = html_response + "<input type='submit' value= 'Submit' />"
        html_response = html_response + "</form>"
        html_response = html_response + "</fieldset>"

    http_response = html_header + html_response + html_footer
    return HttpResponse(http_response)


"""
def get_request_field(request, field_name):
    if field_name in request.args:
        return request.args[field_name]
    elif field_name in request.form:
        return request.form[field_name]
    else:
        return None
"""

def find_numberchoice(request):
    answers=[]
    i=0
    answers.append(request.GET.get('user_answer' + str(i)))
    max_choice=models.max_choice_qcm()
    while(answers[i]==None and i<max_choice):
        i+=1
        answers.append(request.GET.get('user_answer' + str(i)))
    if i==max_choice:
        return -1
    test = models.str_to_list(answers[i])
    question_id=test[1]
    question=models.find_solution_id_mcq(question_id)
    return len(question.text_choice)

def take_quiz(request):
    answers=[]
    answers_list=[]
    number_choice=find_numberchoice(request)
    if number_choice==-1:
        return HttpResponse("Absence de réponse")
    for j in range(number_choice):#Trouver comment trouver le nombre de choix de la question
        answers.append(request.GET.get('user_answer'+str(j)))
    for j in range(number_choice):
        if answers[j]==None:
            None
        else:
            test = models.str_to_list(answers[j])
            answers_list.append(test[0])
            question_id=test[1]
    question=models.find_solution_id_mcq(int(question_id)) #Find question with id=question_id
    if request.method == 'GET':
        if question.take_answer(answers_list):
            return HttpResponse("Correct")
        else:
            return HttpResponse("Wrong")