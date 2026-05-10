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

def discharge_list(request):
    discharges = api_get("discharges")

    if isinstance(discharges, dict):
        discharges = []

    return render(request, "discharges/list.html", {"discharges": discharges})


def discharge_create(request):
    fields = [
        "admission_id", "discharge_date_time", "discharge_condition",
        "final_diagnosis", "discharged_by", "medico_legal_status",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["admission_id"] or not data["discharge_date_time"]:
            context["error_message"] = "Admission ID and Discharge Date are required."
            return render(request, "discharges/create.html", context)

        try:
            api_insert("discharges", data)
            return redirect("discharge_list")
        except Exception:
            context["error_message"] = "Unable to save. Please try again."

    return render(request, "discharges/create.html", context)


def discharge_edit(request, discharge_id):
    discharge = api_get("discharges", params={"discharge_id": discharge_id})

    if not discharge:
        return redirect("discharge_list")

    context = {"form_data": discharge, "error_message": None}

    if request.method == "POST":
        data = {
            "discharge_id":       discharge_id,
            "admission_id":       request.POST.get("admission_id", "").strip(),
            "discharge_date_time": request.POST.get("discharge_date_time", "").strip(),
            "discharge_condition": request.POST.get("discharge_condition", "").strip(),
            "final_diagnosis":    request.POST.get("final_diagnosis", "").strip(),
            "discharged_by":      request.POST.get("discharged_by", "").strip(),
            "medico_legal_status": request.POST.get("medico_legal_status", "").strip(),
        }

        context["form_data"] = data

        if not data["admission_id"] or not data["discharge_date_time"]:
            context["error_message"] = "Admission ID and Discharge Date are required."
            return render(request, "discharges/edit.html", context)

        api_update_full("discharges", data)
        return redirect("discharge_list")

    return render(request, "discharges/edit.html", context)


def discharge_delete(request, discharge_id):
    discharge = api_get("discharges", params={"discharge_id": discharge_id})

    if not discharge:
        return redirect("discharge_list")

    if request.method == "POST":
        api_delete("discharges", {"discharge_id": discharge_id})
        return redirect("discharge_list")

    return render(request, "discharges/delete.html", {"discharge": discharge})


def patientnote_list(request):
    notes = api_get("patientnotes")

    if isinstance(notes, dict):
        notes = []

    return render(request, "patientnotes/list.html", {"notes": notes})


def patientnote_create(request):
    fields = [
        "patient_id", "staff_id", "note_type",
        "content", "created_at",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["note_type"] or not data["content"]:
            context["error_message"] = "Patient ID, Note Type, and Content are required."
            return render(request, "patientnotes/create.html", context)

        try:
            api_insert("patientnotes", data)
            return redirect("patientnote_list")
        except Exception:
            context["error_message"] = "Unable to save. Please try again."

    return render(request, "patientnotes/create.html", context)


def patientnote_edit(request, note_id):
    note = api_get("patientnotes", params={"note_id": note_id})

    if not note:
        return redirect("patientnote_list")

    context = {"form_data": note, "error_message": None}

    if request.method == "POST":
        data = {
            "note_id":    note_id,
            "patient_id": request.POST.get("patient_id", "").strip(),
            "staff_id":   request.POST.get("staff_id", "").strip(),
            "note_type":  request.POST.get("note_type", "").strip(),
            "content":    request.POST.get("content", "").strip(),
            "created_at": request.POST.get("created_at", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["note_type"] or not data["content"]:
            context["error_message"] = "Patient ID, Note Type, and Content are required."
            return render(request, "patientnotes/edit.html", context)

        api_update_full("patientnotes", data)
        return redirect("patientnote_list")

    return render(request, "patientnotes/edit.html", context)


def patientnote_delete(request, note_id):
    note = api_get("patientnotes", params={"note_id": note_id})

    if not note:
        return redirect("patientnote_list")

    if request.method == "POST":
        api_delete("patientnotes", {"note_id": note_id})
        return redirect("patientnote_list")

    return render(request, "patientnotes/delete.html", {"note": note})

def medicalhistory_list(request):
    histories = api_get("medicalhistory")

    if isinstance(histories, dict):
        histories = []

    return render(request, "medicalhistory/list.html", {"histories": histories})


def medicalhistory_create(request):
    fields = [
        "patient_id", "condition_name", "diagnosis_date",
        "is_chronic", "family_history_relevance", "previous_surgeries",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["condition_name"]:
            context["error_message"] = "Patient ID and Condition Name are required."
            return render(request, "medicalhistory/create.html", context)

        try:
            api_insert("medicalhistory", data)
            return redirect("medicalhistory_list")
        except Exception:
            context["error_message"] = "Unable to save. Please try again."

    return render(request, "medicalhistory/create.html", context)


def medicalhistory_edit(request, history_id):
    history = api_get("medicalhistory", params={"history_id": history_id})

    if not history:
        return redirect("medicalhistory_list")

    context = {"form_data": history, "error_message": None}

    if request.method == "POST":
        data = {
            "history_id":               history_id,
            "patient_id":               request.POST.get("patient_id", "").strip(),
            "condition_name":           request.POST.get("condition_name", "").strip(),
            "diagnosis_date":           request.POST.get("diagnosis_date", "").strip(),
            "is_chronic":               request.POST.get("is_chronic", "").strip(),
            "family_history_relevance": request.POST.get("family_history_relevance", "").strip(),
            "previous_surgeries":       request.POST.get("previous_surgeries", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["condition_name"]:
            context["error_message"] = "Patient ID and Condition Name are required."
            return render(request, "medicalhistory/edit.html", context)

        api_update_full("medicalhistory", data)
        return redirect("medicalhistory_list")

    return render(request, "medicalhistory/edit.html", context)


def medicalhistory_delete(request, history_id):
    history = api_get("medicalhistory", params={"history_id": history_id})

    if not history:
        return redirect("medicalhistory_list")

    if request.method == "POST":
        api_delete("medicalhistory", {"history_id": history_id})
        return redirect("medicalhistory_list")

    return render(request, "medicalhistory/delete.html", {"history": history})

def insuranceinfo_list(request):
    insurances = api_get("insuranceinfo")

    if isinstance(insurances, dict):
        insurances = []

    return render(request, "insuranceinfo/list.html", {"insurances": insurances})


def insuranceinfo_create(request):
    fields = [
        "patient_id", "provider_type", "philhealth_no",
        "hmo_name", "policy_number", "is_active", "coverage_limit",
    ]

    context = {"form_data": {}, "error_message": None}

    if request.method == "POST":
        data = {field: request.POST.get(field, "").strip() for field in fields}
        context["form_data"] = data

        if not data["patient_id"] or not data["provider_type"]:
            context["error_message"] = "Patient ID and Provider Type are required."
            return render(request, "insuranceinfo/create.html", context)

        try:
            api_insert("insuranceinfo", data)
            return redirect("insuranceinfo_list")
        except Exception:
            context["error_message"] = "Unable to save. Please try again."

    return render(request, "insuranceinfo/create.html", context)


def insuranceinfo_edit(request, insurance_id):
    insurance = api_get("insuranceinfo", params={"insurance_id": insurance_id})

    if not insurance:
        return redirect("insuranceinfo_list")

    context = {"form_data": insurance, "error_message": None}

    if request.method == "POST":
        data = {
            "insurance_id":   insurance_id,
            "patient_id":     request.POST.get("patient_id", "").strip(),
            "provider_type":  request.POST.get("provider_type", "").strip(),
            "philhealth_no":  request.POST.get("philhealth_no", "").strip(),
            "hmo_name":       request.POST.get("hmo_name", "").strip(),
            "policy_number":  request.POST.get("policy_number", "").strip(),
            "is_active":      request.POST.get("is_active", "").strip(),
            "coverage_limit": request.POST.get("coverage_limit", "").strip(),
        }

        context["form_data"] = data

        if not data["patient_id"] or not data["provider_type"]:
            context["error_message"] = "Patient ID and Provider Type are required."
            return render(request, "insuranceinfo/edit.html", context)

        api_update_full("insuranceinfo", data)
        return redirect("insuranceinfo_list")

    return render(request, "insuranceinfo/edit.html", context)


def insuranceinfo_delete(request, insurance_id):
    insurance = api_get("insuranceinfo", params={"insurance_id": insurance_id})

    if not insurance:
        return redirect("insuranceinfo_list")

    if request.method == "POST":
        api_delete("insuranceinfo", {"insurance_id": insurance_id})
        return redirect("insuranceinfo_list")

    return render(request, "insuranceinfo/delete.html", {"insurance": insurance})