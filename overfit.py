def generate_overfitted_form_instructions(data: dict) -> str:
    """
    this is very overfit to the mock_data, but changing this if the form/json-schema
    changes should be straightforward. the regidity of this prompt engineering
    approach makes it more robust than more open ended approaches. ideally, the
    creation of these sort of prompts would be done automatically in some sort of
    RL gym environment.
    """
    # Attorney Information
    ATTORNEY_ONLINE_ACCOUNT_NUMBER = data["attorney"]["online_account_number"]
    ATTORNEY_FAMILY_NAME = data["attorney"]["family_name"]
    ATTORNEY_FIRST_NAME = data["attorney"]["first_name"]
    ATTORNEY_MIDDLE_NAME = data["attorney"]["middle_name"]
    ATTORNEY_ADDRESS_LINE_1 = data["attorney"]["address_line_1"]
    ATTORNEY_UNIT_TYPE = data["attorney"]["unit_type"]
    ATTORNEY_ADDRESS_LINE_2 = data["attorney"]["address_line_2"]
    ATTORNEY_CITY = data["attorney"]["city"]
    ATTORNEY_STATE = data["attorney"]["state"]
    ATTORNEY_ZIP_CODE = data["attorney"]["zip_code"]
    ATTORNEY_PROVINCE = data["attorney"]["province"]
    ATTORNEY_COUNTRY = data["attorney"]["country"]
    ATTORNEY_DAYTIME_PHONE = data["attorney"]["daytime_phone"]
    ATTORNEY_EMAIL = data["attorney"]["email"]
    ATTORNEY_FAX = data["attorney"]["fax"]
    ATTORNEY_ELIGIBLE = data["attorney"]["attorney_eligible"]
    ATTORNEY_LICENSING_STATE = data["attorney"]["licensing_state"]
    ATTORNEY_BAR_NUMBER = data["attorney"]["bar_number"]
    ATTORNEY_SUBJECT_TO_RESTRICTIONS = data["attorney"][
        "subject_to_restrictions"
    ]  # "no"
    ATTORNEY_LAW_FIRM = data["attorney"]["law_firm"]
    ATTORNEY_IS_NONPROFIT_REP = data["attorney"]["is_nonprofit_rep"]
    ATTORNEY_ORG_NAME = data["attorney"]["org_name"]
    ATTORNEY_ACCREDITATION_DATE = data["attorney"]["accreditation_date"]
    ATTORNEY_ASSOCIATED_WITH_STUDENT = data["attorney"][
        "associated_with_student"
    ]  # "no"
    ATTORNEY_LAW_STUDENT = data["attorney"]["law_student"]
    ATTORNEY_ADMINISTRATIVE_CASE = data["attorney"]["administrative_case"]
    ATTORNEY_ADMINISTRATIVE_MATTER = data["attorney"]["administrative_matter"]
    ATTORNEY_CIVIL_CASE = data["attorney"]["civil_case"]
    ATTORNEY_CIVIL_MATTER = data["attorney"]["civil_matter"]
    ATTORNEY_OTHER_LEGAL = data["attorney"]["other_legal"]
    ATTORNEY_OTHER_LEGAL_MATTER = data["attorney"]["other_legal_matter"]
    ATTORNEY_RECEIPT_NUMBER = data["attorney"]["receipt_number"]
    ATTORNEY_CLIENT_TYPE = data["attorney"]["client_type"]

    # Client Information
    CLIENT_FAMILY_NAME = data["client"]["family_name"]
    CLIENT_FIRST_NAME = data["client"]["first_name"]
    CLIENT_ENTITY_NAME = data["client"]["entity_name"]
    CLIENT_ENTITY_TITLE = data["client"]["entity_title"]
    CLIENT_REFERENCE_NUMBER = data["client"]["reference_number"]
    CLIENT_ID_NUMBER = data["client"]["id_number"]
    CLIENT_DAYTIME_PHONE = data["client"]["daytime_phone"]
    CLIENT_MOBILE_PHONE = data["client"]["mobile_phone"]
    CLIENT_EMAIL = data["client"]["email"]
    CLIENT_ADDRESS_LINE_1 = data["client"]["address_line_1"]
    CLIENT_UNIT_TYPE = data["client"]["unit_type"]
    CLIENT_ADDRESS_LINE_2 = data["client"]["address_line_2"]
    CLIENT_CITY = data["client"]["city"]
    CLIENT_STATE = data["client"]["state"]
    CLIENT_ZIP_CODE = data["client"]["zip_code"]
    CLIENT_PROVINCE = data["client"]["province"]
    CLIENT_COUNTRY = data["client"]["country"]
    CLIENT_SEND_NOTICES_TO_ATTORNEY = data["client"]["send_notices_to_attorney"]
    CLIENT_SEND_DOCUMENTS_TO_ATTORNEY = data["client"]["send_documents_to_attorney"]
    CLIENT_SEND_DOCUMENTS_TO_CLIENT = data["client"]["send_documents_to_client"]
    CLIENT_SIGNATURE_DATE = data["client"]["signature_date"]

    # Top Level Signature Dates
    ATTORNEY_SIGNATURE_DATE = data["attorney_signature_date"]
    ADDITIONAL_SIGNATURE_DATE = data["additional_signature_date"]

    # Part 6 Additional Information (assuming only one entry for this overfitted example)
    ADDITIONAL_INFO_FAMILY_NAME = data["part6"]["additional_info"]["family_name"]
    ADDITIONAL_INFO_GIVEN_NAME = data["part6"]["additional_info"]["given_name"]
    ADDITIONAL_INFO_MIDDLE_NAME = data["part6"]["additional_info"]["middle_name"]
    # Handle the list - assuming exactly one entry as per mock_data
    if data["part6"]["additional_info"]["entries"]:
        ADDITIONAL_INFO_ENTRY_0_PAGE_NUMBER = data["part6"]["additional_info"][
            "entries"
        ][0]["page_number"]
        ADDITIONAL_INFO_ENTRY_0_PART_NUMBER = data["part6"]["additional_info"][
            "entries"
        ][0]["part_number"]
        ADDITIONAL_INFO_ENTRY_0_ITEM_NUMBER = data["part6"]["additional_info"][
            "entries"
        ][0]["item_number"]
        ADDITIONAL_INFO_ENTRY_0_ADDITIONAL_INFO = data["part6"]["additional_info"][
            "entries"
        ][0]["additional_info"]
    else:  # Basic fallback if the list is unexpectedly empty
        ADDITIONAL_INFO_ENTRY_0_PAGE_NUMBER = "[Data Not Provided]"
        ADDITIONAL_INFO_ENTRY_0_PART_NUMBER = "[Data Not Provided]"
        ADDITIONAL_INFO_ENTRY_0_ITEM_NUMBER = "[Data Not Provided]"
        ADDITIONAL_INFO_ENTRY_0_ADDITIONAL_INFO = "[Data Not Provided]"

    instructions = f"""
Please fill out the Form A-28 (Notice of Entry of Appearance as Attorney or Representative) precisely according to the following details. Use the exact values provided and locate fields based on their numbers and labels as shown below.

You should NOT sign the form as a representative of any entity.

**Part 1. Information About Attorney or Representative**

1. Online Account Number (if any): Enter `{ATTORNEY_ONLINE_ACCOUNT_NUMBER}` into field 1.

Name of Attorney or Representative:
2.a. Family Name (Last Name): Enter `{ATTORNEY_FAMILY_NAME}`.
2.b. Given Name (First Name): Enter `{ATTORNEY_FIRST_NAME}`.
2.c. Middle Name: Enter `{ATTORNEY_MIDDLE_NAME}`.

Address of Attorney or Representative:
3.a. Street Number and Name: Enter `{ATTORNEY_ADDRESS_LINE_1}`.
3.b. Unit Type: Select the appropriate checkbox (`Apt.`, `Ste.`, or `Flr.`) based on value `{ATTORNEY_UNIT_TYPE if ATTORNEY_UNIT_TYPE else "[Leave Blank]"}`.
   - Enter the unit number `{ATTORNEY_ADDRESS_LINE_2 if ATTORNEY_ADDRESS_LINE_2 else "[Leave Blank]"}` in the field to the right of the checkboxes.
3.c. City or Town: Enter `{ATTORNEY_CITY}`.
3.d. State: Select `{ATTORNEY_STATE}` from the dropdown.
3.e. ZIP Code: Enter `{ATTORNEY_ZIP_CODE}`.
3.f. Province: Enter `{ATTORNEY_PROVINCE if ATTORNEY_PROVINCE else "[Leave Blank]"}`.
3.g. Postal Code: Enter `{ATTORNEY_ZIP_CODE}`.
3.h. Country: Enter `{ATTORNEY_COUNTRY}`.

Contact Information of Attorney or Representative:
4. Daytime Telephone Number: Enter `{ATTORNEY_DAYTIME_PHONE}`.
5. Mobile Telephone Number (if any): Leave blank as this is not specified in the data.
6. Email Address (if any): Enter `{ATTORNEY_EMAIL}`.
7. Fax Number (if any): Enter `{ATTORNEY_FAX if ATTORNEY_FAX else "[Leave Blank]"}`.

**Part 2. Eligibility Information for Attorney or Representative**

For item 1.a, check the box that says "I am an attorney eligible to practice law in, and a member in good standing of, the bar of the highest courts of the following jurisdictions." based on value `{ATTORNEY_ELIGIBLE}`.

Licensing Authority: Enter `{ATTORNEY_LICENSING_STATE}` in the field below "Licensing Authority".
1.b. Bar Number (if applicable): Enter `{ATTORNEY_BAR_NUMBER}`.

1.c. Select only one box:
- Check "am not" for "I am not subject to any order suspending, enjoining, restraining, disbarring, or otherwise restricting me in the practice of law" based on the value `{ATTORNEY_SUBJECT_TO_RESTRICTIONS}`.

1.d. Name of Law Firm or Organization (if applicable): Enter `{ATTORNEY_LAW_FIRM}`.

For item 2.a, do NOT check the box related to nonprofit organization representation based on value `{ATTORNEY_IS_NONPROFIT_REP}`.
2.b. Name of Recognized Organization: Leave blank based on the above.
2.c. Date of Accreditation: Leave blank based on the above.

For item 3, do NOT check the box that says "I am associated with..." based on value `{ATTORNEY_ASSOCIATED_WITH_STUDENT}`.

For item 4.a, do NOT check the box related to being a law student based on the above.
4.b. Name of Law Student or Law Graduate: Leave blank based on the above.

**Part 3. Notice of Appearance as Attorney or Representative**

This appearance relates to matters before (select applicable option):
- If `{ATTORNEY_ADMINISTRATIVE_CASE}` is True, check box 1.a. "Administrative Case"
  In field 1.b, enter the specific matter: `{ATTORNEY_ADMINISTRATIVE_MATTER}`.
- If `{ATTORNEY_CIVIL_CASE}` is True, check box 2.a. "Civil Case"
  Otherwise, leave unchecked.
  Field 2.b: Leave blank or enter `{ATTORNEY_CIVIL_MATTER if ATTORNEY_CIVIL_MATTER else "[Leave Blank]"}`.
- If `{ATTORNEY_OTHER_LEGAL}` is True, check box 3.a. "Other Legal Matter"
  Otherwise, leave unchecked.
  Field 3.b: Leave blank or enter `{ATTORNEY_OTHER_LEGAL_MATTER if ATTORNEY_OTHER_LEGAL_MATTER else "[Leave Blank]"}`.

4. Receipt Number (if any): Enter `{ATTORNEY_RECEIPT_NUMBER}`.

5. I enter my appearance as an attorney or accredited representative at the request of the (select only one box):
- Check the appropriate box that corresponds to `{ATTORNEY_CLIENT_TYPE}` (Applicant, Petitioner, Requestor, Beneficiary/Derivative, or Respondent).

Information About Client:
6.a. Family Name (Last Name): Enter `{CLIENT_FAMILY_NAME}`.
6.b. Given Name (First Name): Enter `{CLIENT_FIRST_NAME}`.
6.c. Middle Name: Leave blank (not provided in data).
7.a. Name of Entity (if applicable): Enter `{CLIENT_ENTITY_NAME if CLIENT_ENTITY_NAME else "[Leave Blank]"}`.
7.b. Title of Authorized Signatory for Entity (if applicable): Enter `{CLIENT_ENTITY_TITLE if CLIENT_ENTITY_TITLE else "[Leave Blank]"}`.
8. Client's Reference Number (if any): Enter `{CLIENT_REFERENCE_NUMBER if CLIENT_REFERENCE_NUMBER else "[Leave Blank]"}`.
9. Client's ID Number (if any): Enter `{CLIENT_ID_NUMBER}`.

Client's Contact Information:
10. Daytime Telephone Number: Enter `{CLIENT_DAYTIME_PHONE}`.
11. Mobile Telephone Number (if any): Enter `{CLIENT_MOBILE_PHONE if CLIENT_MOBILE_PHONE else "[Leave Blank]"}`.
12. Email Address (if any): Enter `{CLIENT_EMAIL}`.

Mailing Address of Client:
13.a. Street Number and Name: Enter `{CLIENT_ADDRESS_LINE_1}`.
13.b. Unit Type: Select the appropriate checkbox (Apt., Ste., or Flr.) based on `{CLIENT_UNIT_TYPE if CLIENT_UNIT_TYPE else "[Leave Blank]"}`.
    - Enter the unit number `{CLIENT_ADDRESS_LINE_2 if CLIENT_ADDRESS_LINE_2 else "[Leave Blank]"}` in the field to the right of the checkboxes.
13.c. City or Town: Enter `{CLIENT_CITY}`.
13.d. State: Select `{CLIENT_STATE}` from the dropdown.
13.e. ZIP Code: Enter `{CLIENT_ZIP_CODE}`.
13.f. Province: Enter `{CLIENT_PROVINCE if CLIENT_PROVINCE else "[Leave Blank]"}`.
13.g. Postal Code: Enter `{CLIENT_ZIP_CODE}`.
13.h. Country: Enter `{CLIENT_COUNTRY}`.

**Part 4. Client's Consent to Representation and Signature**

For the checkboxes under "Options Regarding Receipt of Notices and Documents":
- If `{CLIENT_SEND_NOTICES_TO_ATTORNEY}` is "Y", check box 1.a. "I request that all original notices on an application or petition be sent to the business address of my attorney or representative."
- If `{CLIENT_SEND_DOCUMENTS_TO_ATTORNEY}` is "Y", check box 1.b. "I request that any important documents that I receive be sent to the business address of my attorney or representative."
- If `{CLIENT_SEND_DOCUMENTS_TO_CLIENT}` is "Y", check box 1.c. "I request that important documentation be sent to me at my mailing address." Otherwise, leave unchecked.

2.b. Date of Signature (mm/dd/yyyy): Enter `{CLIENT_SIGNATURE_DATE if CLIENT_SIGNATURE_DATE else "[Leave Blank]"}`.

**Part 5. Signature of Attorney or Representative**

1.b. Date of Signature (mm/dd/yyyy): Enter `{ATTORNEY_SIGNATURE_DATE if ATTORNEY_SIGNATURE_DATE else "[Leave Blank]"}`.
2.b. Date of Signature (mm/dd/yyyy): Enter `{ADDITIONAL_SIGNATURE_DATE if ADDITIONAL_SIGNATURE_DATE else "[Leave Blank]"}`.

**Part 6. Additional Information**

1.a. Family Name (Last Name): Enter `{ADDITIONAL_INFO_FAMILY_NAME}`.
1.b. Given Name (First Name): Enter `{ADDITIONAL_INFO_GIVEN_NAME}`.
1.c. Middle Name: Enter `{ADDITIONAL_INFO_MIDDLE_NAME}`.

In the additional information section:
2.a. Page Number: Enter `{ADDITIONAL_INFO_ENTRY_0_PAGE_NUMBER}`.
2.b. Part Number: Enter `{ADDITIONAL_INFO_ENTRY_0_PART_NUMBER}`.
2.c. Item Number: Enter `{ADDITIONAL_INFO_ENTRY_0_ITEM_NUMBER}`.
- In the large text field below these entries, enter: "{ADDITIONAL_INFO_ENTRY_0_ADDITIONAL_INFO}"

If you need to enter more additional information, use sections 3.a through 3.c in the same manner as above.

Ensure all fields are completed exactly as specified. If a value is indicated as '[Leave Blank]', ensure the corresponding field is left empty. Double-check all entries before submitting.
"""
    return instructions


# --- Example Usage with the provided mock_data ---
if __name__ == "__main__":
    from data import MOCK_DATA

    # Generate the instructions
    instructions_string = generate_overfitted_form_instructions(MOCK_DATA)

    # Print the generated instructions
    print(instructions_string)
