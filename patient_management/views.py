from django.shortcuts import render, redirect
from .services.api import api_get, api_insert, api_delete, api_update_partial, api_update_full

# Create your views here.
def home(request):
    return render(request, "home.html")

def patient_list(request):
    patients = api_get("patients") 

    if isinstance(patients, dict):
        patients = []

    return render(request, "patients/list.html", {"patients": patients})

def patient_create(request):
    fields = [ 
        "hrn",
        "first_name",
        "middle_name",
        "last_name",
        "suffix",
        "birth_date",
        "gender",
        "civil_status",
        "blood_type",
        "nationality",
        "religion", 
        "occupation",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        try:
            api_insert("patients", data)
            return redirect("patient_list")
        except Exception:
            context["error_message"] = "Unable to create patient right now. Please try again."

    return render(request, "patients/create.html", context)



def patient_edit(request, patient_id):
    # the API returns a single object directly, not a list
    patient = api_get("patients", params={"patient_id": patient_id})

    # if patient not found or API returned empty
    if not patient:
        return redirect("patient_list")

    context = {
        "form_data": patient,
        "error_message": None
    }

    if request.method=="POST":

        data = {
            "patient_id": patient_id,
            "hrn": request.POST.get("hrn", "").strip(),
            "first_name": request.POST.get("first_name", "").strip(),
            "middle_name": request.POST.get("middle_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "suffix": request.POST.get("suffix", "").strip(),
            "birth_date": request.POST.get("birth_date", "").strip(),
            "gender": request.POST.get("gender", "").strip(),
            "civil_status": request.POST.get("civil_status", "").strip(),
            "blood_type": request.POST.get("blood_type", "").strip(),
            "nationality": request.POST.get("nationality", "").strip(),
            "religion": request.POST.get("religion", "").strip(),
            "occupation": request.POST.get("occupation", "").strip(),
        }

        context["form_data"] = data

        if not data["hrn"] or not data["first_name"] or not data["last_name"]:
            context["error_message"] = "HRN, First Name, Middle Name, and Last Name are required"
            return render(request, "patients/edit.html", context)

        api_update_full("patients", data)
        return redirect("patient_list")
    
    return render(request, "patients/edit.html", context)


def patient_delete(request, patient_id):

    patient = api_get("patients", params={"patient_id": patient_id})

    if not patient:
        return redirect("patient_list")

    if request.method == "POST":
        api_delete("patients", {"patient_id": patient_id})
        return redirect("patient_list")

    return render(request, "patients/delete.html", {"patient": patient})

 