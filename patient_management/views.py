from django.shortcuts import render, redirect
from .services.api import api_get, api_insert, api_delete, api_update_partial, api_update_full

# Create your views here.
def home(request):
    patients = api_get("patients")
    admissions = api_get("admissions")
    allergies = api_get("allergies")

    if isinstance(patients, dict):
        patients = []

    if isinstance(admissions, dict):
        admissions = []

    if isinstance(allergies, dict):
        allergies = []

    recent_patients = patients[-5:] if patients else []
    recent_admissions = admissions[-5:] if admissions else []

    return render(request, "home.html", {
        "recent_patients": recent_patients,
        "recent_admissions": recent_admissions,
    })
    

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


def address_list(request):
    addresses = api_get("addresses")

    if isinstance(addresses, dict):
        addresses = []

    return render(request, "addresses/list.html", {"addresses": addresses})


def address_create(request):
    fields = [
        "patient_id",
        "address_type",
        "street_subdivision",
        "barangay",
        "city_municipality",
        "province",
        "zip_code",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["address_type"]:
            context["error_message"] = "Patient ID and Address Type are required."
            return render(request, "addresses/create.html", context)

        try:
            api_insert("addresses", data)
            return redirect("address_list")
        except Exception:
            context["error_message"] = "Unable to create address right now."

    return render(request, "addresses/create.html", context)


def address_edit(request, address_id):
    result = api_get("addresses", params={"address_id": address_id})

    # If API returns a list, get the first address
    if isinstance(result, list) and len(result) > 0:
        address = result[0]
    else:
        address = result

    if not address:
        return redirect("address_list")

    context = {
        "form_data": address,
        "error_message": None,
        "address_id": address_id,
    }

    if request.method == "POST":
        data = {
            "address_id": address_id,
            "patient_id": request.POST.get("patient_id", "").strip(),
            "address_type": request.POST.get("address_type", "").strip(),
            "street_subdivision": request.POST.get("street_subdivision", "").strip(),
            "barangay": request.POST.get("barangay", "").strip(),
            "city_municipality": request.POST.get("city_municipality", "").strip(),
            "province": request.POST.get("province", "").strip(),
            "zip_code": request.POST.get("zip_code", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["address_type"]:
            context["error_message"] = "Patient ID and Address Type are required."
            return render(request, "addresses/edit.html", context)

        try:
            api_update_full("addresses", data)
            return redirect("address_list")
        except Exception:
            context["error_message"] = "Unable to update address right now."

    return render(request, "addresses/edit.html", context)


def address_delete(request, address_id):
    result = api_get("addresses", params={"address_id": address_id})

    if isinstance(result, list) and len(result) > 0:
        address = result[0]
    else:
        address = result

    if not address:
        return redirect("address_list")

    if request.method == "POST":
        api_delete("addresses", {"address_id": address_id})
        return redirect("address_list")

    return render(request, "addresses/delete.html", {"address": address})


def emergencycontact_list(request):
    contacts = api_get("emergencycontacts")

    if isinstance(contacts, dict):
        contacts = []

    return render(request, "emergencycontacts/list.html", {"contacts": contacts})


def emergencycontact_create(request):
    fields = [
        "patient_id",
        "name",
        "relationship",
        "contact_number",
        "is_next_of_kin",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["name"] or not data["contact_number"]:
            context["error_message"] = "Patient ID, Name, and Contact Number are required."
            return render(request, "emergencycontacts/create.html", context)

        try:
            api_insert("emergencycontacts", data)
            return redirect("emergencycontact_list")
        except Exception:
            context["error_message"] = "Unable to create emergency contact right now."

    return render(request, "emergencycontacts/create.html", context)



def emergencycontact_edit(request, contact_id):
    result = api_get("emergencycontacts", params={"contact_id": contact_id})

    if isinstance(result, list) and len(result) > 0:
        contact = result[0]
    else:
        contact = result

    if not contact:
        return redirect("emergencycontact_list")

    context = {
        "form_data": contact,
        "error_message": None,
        "contact_id": contact_id,
    }

    if request.method == "POST":
        data = {
            "contact_id": contact_id,
            "patient_id": request.POST.get("patient_id", "").strip(),
            "name": request.POST.get("name", "").strip(),
            "relationship": request.POST.get("relationship", "").strip(),
            "contact_number": request.POST.get("contact_number", "").strip(),
            "is_next_of_kin": request.POST.get("is_next_of_kin", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["name"] or not data["contact_number"]:
            context["error_message"] = "Patient ID, Name, and Contact Number are required."
            return render(request, "emergencycontacts/edit.html", context)

        try:
            api_update_full("emergencycontacts", data)
            return redirect("emergencycontact_list")
        except Exception:
            context["error_message"] = "Unable to update emergency contact right now."

    return render(request, "emergencycontacts/edit.html", context)


def emergencycontact_delete(request, contact_id):
    result = api_get("emergencycontacts", params={"contact_id": contact_id})

    if isinstance(result, list) and len(result) > 0:
        contact = result[0]
    else:
        contact = result

    if not contact:
        return redirect("emergencycontact_list")

    if request.method == "POST":
        api_delete("emergencycontacts", {"contact_id": contact_id})
        return redirect("emergencycontact_list")

    return render(request, "emergencycontacts/delete.html", {"contact": contact})



def guardian_list(request):
    guardians = api_get("guardians")

    if isinstance(guardians, dict):
        guardians = []

    return render(request, "guardians/list.html", {"guardians": guardians})


def guardian_create(request):
    fields = [
        "patient_id",
        "full_name",
        "relationship",
        "is_legal_representative",
        "contact_info",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["full_name"] or not data["relationship"]:
            context["error_message"] = "Patient ID, Full Name, and Relationship are required."
            return render(request, "guardians/create.html", context)

        try:
            api_insert("guardians", data)
            return redirect("guardian_list")
        except Exception:
            context["error_message"] = "Unable to create guardian right now."

    return render(request, "guardians/create.html", context)



def guardian_edit(request, guardian_id):
    result = api_get("guardians", params={"guardian_id": guardian_id})

    if isinstance(result, list) and len(result) > 0:
        guardian = result[0]
    else:
        guardian = result

    if not guardian:
        return redirect("guardian_list")

    context = {
        "form_data": guardian,
        "error_message": None,
        "guardian_id": guardian_id,
    }

    if request.method == "POST":
        data = {
            "guardian_id": guardian_id,
            "patient_id": request.POST.get("patient_id", "").strip(),
            "full_name": request.POST.get("full_name", "").strip(),
            "relationship": request.POST.get("relationship", "").strip(),
            "is_legal_representative": request.POST.get("is_legal_representative", "").strip(),
            "contact_info": request.POST.get("contact_info", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["full_name"] or not data["relationship"]:
            context["error_message"] = "Patient ID, Full Name, and Relationship are required."
            return render(request, "guardians/edit.html", context)

        try:
            api_update_full("guardians", data)
            return redirect("guardian_list")
        except Exception:
            context["error_message"] = "Unable to update guardian right now."

    return render(request, "guardians/edit.html", context)


def guardian_delete(request, guardian_id):
    result = api_get("guardians", params={"guardian_id": guardian_id})

    if isinstance(result, list) and len(result) > 0:
        guardian = result[0]
    else:
        guardian = result

    if not guardian:
        return redirect("guardian_list")

    if request.method == "POST":
        api_delete("guardians", {"guardian_id": guardian_id})
        return redirect("guardian_list")

    return render(request, "guardians/delete.html", {"guardian": guardian})



def admission_list(request):
    admissions = api_get("admissions")

    if isinstance(admissions, dict):
        admissions = []

    return render(request, "admissions/list.html", {"admissions": admissions})


def admission_create(request):
    fields = [
        "patient_id",
        "case_no",
        "admission_date_time",
        "admitting_doctor_id",
        "initial_diagnosis",
        "ward_room_id",
        "admission_source",
        "chief_complaint",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["case_no"] or not data["admission_date_time"]:
            context["error_message"] = "Patient ID, Case No, and Admission Date/Time are required."
            return render(request, "admissions/create.html", context)

        try:
            api_insert("admissions", data)
            return redirect("admission_list")
        except Exception:
            context["error_message"] = "Unable to create admission right now."

    return render(request, "admissions/create.html", context)


def admission_edit(request, admission_id):
    result = api_get("admissions", params={"admission_id": admission_id})

    if isinstance(result, list) and len(result) > 0:
        admission = result[0]
    else:
        admission = result

    if not admission:
        return redirect("admission_list")

    context = {
        "form_data": admission,
        "error_message": None,
        "admission_id": admission_id,
    }

    if request.method == "POST":
        data = {
            "admission_id": admission_id,
            "patient_id": request.POST.get("patient_id", "").strip(),
            "case_no": request.POST.get("case_no", "").strip(),
            "admission_date_time": request.POST.get("admission_date_time", "").strip(),
            "admitting_doctor_id": request.POST.get("admitting_doctor_id", "").strip(),
            "initial_diagnosis": request.POST.get("initial_diagnosis", "").strip(),
            "ward_room_id": request.POST.get("ward_room_id", "").strip(),
            "admission_source": request.POST.get("admission_source", "").strip(),
            "chief_complaint": request.POST.get("chief_complaint", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["case_no"] or not data["admission_date_time"]:
            context["error_message"] = "Patient ID, Case No, and Admission Date/Time are required."
            return render(request, "admissions/edit.html", context)

        try:
            api_update_full("admissions", data)
            return redirect("admission_list")
        except Exception:
            context["error_message"] = "Unable to update admission right now."

    return render(request, "admissions/edit.html", context)


def admission_delete(request, admission_id):
    result = api_get("admissions", params={"admission_id": admission_id})

    if isinstance(result, list) and len(result) > 0:
        admission = result[0]
    else:
        admission = result

    if not admission:
        return redirect("admission_list")

    if request.method == "POST":
        api_delete("admissions", {"admission_id": admission_id})
        return redirect("admission_list")

    return render(request, "admissions/delete.html", {"admission": admission})


def allergy_list(request):
    allergies = api_get("allergies")

    if isinstance(allergies, dict):
        allergies = []

    return render(request, "allergies/list.html", {"allergies": allergies})


def allergy_create(request):
    fields = [
        "patient_id",
        "allergen",
        "reaction_severity",
        "symptoms",
        "recorded_date",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["allergen"]:
            context["error_message"] = "Patient ID and Allergen are required."
            return render(request, "allergies/create.html", context)

        try:
            api_insert("allergies", data)
            return redirect("allergy_list")
        except Exception:
            context["error_message"] = "Unable to create allergy."

    return render(request, "allergies/create.html", context)


def allergy_edit(request, allergy_id):
    result = api_get("allergies", params={"allergy_id": allergy_id})

    if isinstance(result, list) and len(result) > 0:
        allergy = result[0]
    else:
        allergy = result

    if not allergy:
        return redirect("allergy_list")

    context = {
        "form_data": allergy,
        "error_message": None,
        "allergy_id": allergy_id,
    }

    if request.method == "POST":
        data = {
            "allergy_id": allergy_id,
            "patient_id": request.POST.get("patient_id", "").strip(),
            "allergen": request.POST.get("allergen", "").strip(),
            "reaction_severity": request.POST.get("reaction_severity", "").strip(),
            "symptoms": request.POST.get("symptoms", "").strip(),
            "recorded_date": request.POST.get("recorded_date", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["allergen"]:
            context["error_message"] = "Patient ID and Allergen are required."
            return render(request, "allergies/edit.html", context)

        try:
            api_update_full("allergies", data)
            return redirect("allergy_list")
        except Exception:
            context["error_message"] = "Unable to update allergy."

    return render(request, "allergies/edit.html", context)


def allergy_delete(request, allergy_id):
    result = api_get("allergies", params={"allergy_id": allergy_id})

    if isinstance(result, list) and len(result) > 0:
        allergy = result[0]
    else:
        allergy = result

    if not allergy:
        return redirect("allergy_list")

    if request.method == "POST":
        api_delete("allergies", {"allergy_id": allergy_id})
        return redirect("allergy_list")

    return render(request, "allergies/delete.html", {"allergy": allergy})