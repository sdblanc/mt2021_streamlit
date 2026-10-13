# Appendix: Horus Software API reference (rendered)

Source: Notion export of the Horus documentation pages (Welcome page + API Reference pages; docs updated 2026-09-24), uploaded by Silas to Google Drive as 'horus' on 13 Oct 2026, plus the book-entries.info page supplied separately the same day. Each page embeds an OpenAPI 3.0.3 fragment; these were merged (72 unique endpoints; book-entries.list appeared twice, identical) and rendered mechanically below. '*' = required. The guide pages are in appendix_horus_guides.md.

## Welcome page (verbatim)

#### **Welcome to the Horus Software API**Read and write accounting data in Horus Office from your own application.

The **Horus Software API** lets your application read and update the data of a **Horus Office** database: accounting folders, customers and suppliers, chart of accounts, book entries, invoices, documents and more.

It is designed for software vendors and integrators who want to connect their product to the accounting records that fiduciaries and SMBs manage in Horus Office.

# **What you can build**

- **Invoicing, e-commerce or expense tools** that push sales and purchase invoices, with their PDF, straight into the accounting.
- **Document collection** flows that send PDFs, images, XML, CODA or SODA files to be processed automatically into book entries.
- **CRM or ERP synchronisation** of customers and suppliers.
- **Reporting, dashboards and credit control** based on ledgers, balances and outstanding items.
- **Payment reconciliation** by matching payments with open invoices.

# **The API at a glance**

|  |  |
| --- | --- |
| Protocol | HTTPS, JSON-RPC style methods such as `companies.list` or `invoices.sales.new` |
| Data format | JSON (requests and responses), `multipart/form-data` for file uploads |
| Authentication | OAuth 2 authorization code flow, Bearer access tokens valid for 1 hour |
| Base URL | **Different for each license**, obtained during authorization as `api_url` |
| Identifiers | GUIDs, plus human-readable search keys for accounts, daybooks, companies… |

> 📘
> 
> 
> ### **One license, one API URL**
> 
> Each fiduciary or SMB using Horus Office has its own database and its **own API endpoint**. Your integration discovers it during the authorization flow and must never hard-code it. The [Authentication overview](https://docs.horus-software.be/docs/authentication-overview) explains how it works.
> 

# **Where to start**

1. [Register your integration](https://docs.horus-software.be/docs/register-your-integration) to get your credentials.
2. Follow the [Quickstart](https://docs.horus-software.be/docs/quickstart) to connect a license and make your first calls.
3. Read the [Core Concepts](https://docs.horus-software.be/docs/making-requests) and the [data model](https://docs.horus-software.be/docs/data-model) before building your integration.

# **How this documentation is organised**

| **Section** | **Content** |
| --- | --- |
| **Getting Started** | Registration and a step-by-step first connection. |
| **Authentication** | The OAuth 2 flow, the license-specific API URL and the token lifecycle. |
| **Core Concepts** | Request and response conventions, errors, sideloading and the Horus data model. |
| **Working with Accounting Data** | Task-oriented guides: reading data, managing companies, posting invoices and operations, documents, matching. |
| **Tools & Resources** | Testing with the API Reference and Postman, versioning policy and support. |

The **API Reference** tab documents every endpoint with its parameters, schemas and examples.

# **Need help?**

Write to [developer@horus-software.be](mailto:developer@horus-software.be). See [Support & FAQ](https://docs.horus-software.be/docs/support) for what to include in your message.

[licenses.me](http://licenses.me/)

## Endpoints

```text

==========================================================================================
## GET /licenses.me   [tags: Licenses]
PAGE TEXT: Get the license linked to the current authenticated user.
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="5c7d4294-1e95-4b9f-a2ee-0a3e84ca836b"]  // 
      - LicenseName: string [example="John's Pizzas"]  // 
      - LicenseKey: string [example="jd8g53"]  // 
      - CreationDate: string(date-time) [example="2018-04-01T12:12:33+00:00"]  // 
      - Language: string enum["FR", "NL"] [example="FR"]  // 
      - IsMain: boolean [example=false]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /licenses.main   [tags: Licenses]
PAGE TEXT: Get the main license, i.e. the fiduciary/SMB license.
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="7d6aaf7c-29b8-4865-a0fe-525a517611b7"]  // 
      - LicenseName: string [example="Fiduciary 123"]  // 
      - LicenseKey: string [example="6df4r1"]  // 
      - CreationDate: string(date-time) [example="2018-03-16T15:26:42+00:00"]  // 
      - Language: string enum["FR", "NL"] [example="FR"]  // 
      - IsMain: boolean [example=false]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /users.me   [tags: Users]
PAGE TEXT: Get the current authenticated user.
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="14feb291-8b47-44c6-8cbb-97a3f24c33c8"]  // 
      - FirstName: string [example="Robert"]  // 
      - LastName: string [example="Doe"]  // 
      - Email: string [example="robert@fiduciary.example"]  // 
      - CreationDate: string(date-time) [example="2018-03-16T15:16:35+00:00"]  // 
      - PhoneNumber: string|null [example="0497/12 34 56"]  // 
      - Language: string enum["FR", "NL"] [example="FR"]  // 
      - IsAccountant: boolean [example=true]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /users.list   [tags: Users]
PAGE TEXT: Get a list of users linked to the same licence as the current authenticated user.
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="14feb291-8b47-44c6-8cbb-97a3f24c33c8"]  // 
      - FirstName: string [example="Robert"]  // 
      - LastName: string [example="Doe"]  // 
      - Email: string [example="robert@fiduciary.example"]  // 
      - CreationDate: string(date-time) [example="2018-03-16T15:16:35+00:00"]  // 
      - PhoneNumber: string|null [example="0497/12 34 56"]  // 
      - Language: string enum["FR", "NL"] [example="FR"]  // 
      - IsAccountant: boolean [example=true]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /users.info   [tags: Users]
PAGE TEXT: Get a specific user.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="14feb291-8b47-44c6-8cbb-97a3f24c33c8"]  // 
      - FirstName: string [example="Robert"]  // 
      - LastName: string [example="Doe"]  // 
      - Email: string [example="robert@fiduciary.example"]  // 
      - CreationDate: string(date-time) [example="2018-03-16T15:16:35+00:00"]  // 
      - PhoneNumber: string|null [example="0497/12 34 56"]  // 
      - Language: string enum["FR", "NL"] [example="FR"]  // 
      - IsAccountant: boolean [example=true]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /folders.list   [tags: Folders]
PAGE TEXT: Get a list of folders.
REQUEST BODY (application/json) required: object
  - Mode *: number enum[0, 1]  // - `0`: All folders - For the accountant: All folders. - For the entrepreneur: All folders to which she/he has access. - `1`: My folders - For the accountant: All folders for which she/he is responsible. - For the entrepreneur: All folders to which she/he has access.
  - Filter: object|null  // All filters on *strings* are performed using the *contains* clause. The folder must match **all specified** filters in order to be included in the response.
      - SearchKey: string [example="REDCORP"]  // Filters on search keys
      - FolderName: string [example="RedCorp SPRL"]  // Filters on folder names
      - Legislation: string enum["BE", "LU"] [example="BE"]  // Filters on the legislation
      - Language: string enum["FR", "NL", "DE", "XX"] [example="FR"]  // 
      - IsVatLiable: boolean [example=true]  // Filters on folders being VAT liable or not.
      - VatNumber: string [example="BE0000000097"]  // Filters on the VAT number using the *equals* clause - *IsVatLiable* must be set to *true*
      - Address: string [example="Quai des ardennes, 9"]  // Filters on the address
      - IsPrivate: boolean [example=false]  // Filters on folders being private or not
      - WithAssets: boolean [example=true]  // Filters on folders with *Assets* module or not
      - WithAnalytics: boolean [example=false]  // Filters on folders with *Analytics* module or not
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - CreationDate: string(date-time) [example="2018-03-20T09:46:23+00:00"]  // 
      - SearchKey: string [example="REDCORP"]  // 
      - FolderName: string [example="RedCorp SPRL"]  // 
      - Legislation: string enum["BE", "LU"] [example="BE"]  // 
      - Language: string enum["FR", "NL", "DE", "XX"] [example="FR"]  // 
      - AlternateLanguage: string enum["FR", "NL", "DE", "XX"] [example="NL"]  // 
      - IsVatLiable: boolean [example=true]  // 
      - VatNumber: string|null [example="BE0000000097"]  // 
      - Address: string [example="Quai des ardennes, 9"]  // 
      - ZipCode: string [example="4020"]  // 
      - Locality: string [example="Liège"]  // 
      - IsPrivate: boolean [example=false]  // 
      - ContactName: string|null  // 
      - ContactEmail: string|null [example="info@redcorp.be"]  // 
      - ContactPhone: string|null  // 
      - ContactMobilePhone: string|null  // 
      - WithAssets: boolean [example=true]  // 
      - WithAnalytics: boolean [example=false]  // 
      - ResponsibleUser: object  // 
          - Type: string [example="Users"]  // 
          - Id: string [example="14feb291-8b47-44c6-8cbb-97a3f24c33c8"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /folders.info   [tags: Folders]
PAGE TEXT: Get details for a specific folder.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - CreationDate: string(date-time) [example="2018-03-20T09:46:23+00:00"]  // 
      - SearchKey: string [example="REDCORP"]  // 
      - FolderName: string [example="RedCorp SPRL"]  // 
      - Legislation: string enum["BE", "LU"] [example="BE"]  // 
      - Language: string enum["FR", "NL", "DE", "XX"] [example="FR"]  // 
      - AlternateLanguage: string enum["FR", "NL", "DE", "XX"] [example="NL"]  // 
      - IsVatLiable: boolean [example=true]  // 
      - VatNumber: string|null [example="BE0000000097"]  // 
      - Address: string [example="Quai des ardennes, 9"]  // 
      - ZipCode: string [example="4020"]  // 
      - Locality: string [example="Liège"]  // 
      - CountryCode: string [example="BE"]  // 
      - IsPrivate: boolean [example=false]  // 
      - ContactName: string|null  // 
      - ContactEmail: string|null [example="info@redcorp.be"]  // 
      - ContactPhone: string|null  // 
      - ContactMobilePhone: string|null  // 
      - WithAssets: boolean [example=true]  // 
      - WithAnalytics: boolean [example=false]  // 
      - ResponsibleUser: object  // 
          - Type: string [example="Users"]  // 
          - Id: string [example="14feb291-8b47-44c6-8cbb-97a3f24c33c8"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /companies.list   [tags: Companies]
PAGE TEXT: Get a list of companies for a folder.
(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
OP DESCRIPTION: Get a list of companies for a folder.

(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
REQUEST BODY (application/json) required: object
  - FolderId *: string  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The company must match **all specified** filters in order to be included in the response.
      - Id: string  // Filters on a specific company id
      - SearchKey: string [example="Horus"]  // Filters on search keys
      - Name: string [example="Horus Software"]  // Filters on company names
      - Language: string enum["FR", "NL", "DE", "EN", "ES", "PT", "XX"] [example="FR"]  // 
      - IsVatLiable: boolean [example=true]  // Filters on companies being VAT liable or not.
      - VatNumber: string [example="BE0478696879"]  // Filters on the VAT number using the *equals* clause - *IsVatLiable* must be set to *true*
      - Iban: string [example="BE68539007547034"]  // Filters on the IBAN using the *equals* clause
      - Address: string [example="Quai des ardennes, 9"]  // Filters on the address
      - IsBadDebtor: boolean  // 
      - IsCustomer: boolean  // 
      - IsSupplier: boolean  // 
      - IsBeneficiary: boolean  // 
      - Family: string  // 
      - ExternalReference: string  // 
      - Email: string  // Filters on an email address (contact, invoice or reminder email address)
      - UsualCustomerPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
      - UsualSupplierPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
      - ModifiedAfter: string(date-time) [example="2021-01-01T00:00:00+00:00"]  // *NULL* by default. Include only companies modified after a given date.
      - ModifiedBefore: string(date-time) [example="2022-01-01T00:00:00+00:00"]  // *NULL* by default. Include only companies modified before a given date.
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
      - SearchKey: string [example="HORUS"]  // 
      - Name: string [example="Horus Software"]  // 
      - Name2: string|null  // 
      - Address: string [example="Quai des ardennes, 9"]  // 
      - Address2: string  // 
      - ZipCode: string [example="4020"]  // 
      - Locality: string [example="Liège"]  // 
      - CountryCode: string [example="BE"]  // 
      - IsVatLiable: boolean [example=true]  // 
      - VatNumber: string|null [example="BE0478696879"]  // Only if 'IsVatLiable' is true.
      - EnterpriseNumber: string|null  // Only if 'IsVatLiable' is false.
      - CurrencyCode: string|null  // 
      - Language: string enum["FR", "NL", "DE", "EN", "ES", "PT", "XX"] [example="FR"]  // 
      - ContactName: string|null  // 
      - ContactEmail: string|null [example="info@horus-software.be"]  // 
      - ContactPhone: string|null  // 
      - ContactWebsite: string|null [example="<https://horussoftware.be>"]  // 
      - InvoiceEmail: string [example="invoices@horus-software.be"]  // 
      - ReminderEmail: string [example="reminders@horus-software.be"]  // 
      - IsBadDebtor: boolean [example=false]  // 
      - IsCustomer: boolean [example=true]  // 
      - IsSupplier: boolean [example=false]  // 
      - IsBeneficiary: boolean [example=false]  // 
      - BeneficiaryInfo: object|null  // NULL if 'IsBeneficiary' is set to 'False'.
          - BeneficiaryType: number enum[0, 10, 20, 30, 40]  // - `0`: Undefined - `10`: Employee - `20`: Manager - `30`: Freelance - `40`: Third party
          - Inactive: boolean [example=false]  // 
          - InactiveSince: string|null  // 
          - FirstName *: string [example="John"]  // 
          - LastName *: string [example="Doe"]  // 
          - Email: string [example="john.doe@gmail.com"]  // 
          - DefaultComment: string [example="Your salary for this month"]  // 
          - DefaultSalaryAmount: number|null [example=3000]  // 
          - DefaultCurrentAccount: object|null  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="8155faa5-187c-48e8-b50b-7e815f58ff5e"]  // 
          - DefaultSalaryAccount: object|null  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="409b3629-5895-40ea-88b1-7db371a5bc32"]  // 
      - UsualCustomerPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
      - UsualSupplierPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
      - CustomerActivitySuspended: boolean [example=false]  // 
      - CustomerDomiciliationReference: string|null  // 
      - CustomerDomiciliationStartDate: string|null  // 
      - CustomerDomiciliationType: number enum[0, 1]  // - `0`: CORE - `1`: B2B
      - CustomerPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
      - SupplierPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
      - Family: string|null  // 
      - ExternalReference: string|null  // 
      - LastModifiedDate: string(date-time) [example="2021-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
      - MainIban: object|null  // 
          - Type: string [example="Ibans"]  // 
          - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - DomiciliationIban: object|null  // 
          - Type: string [example="Ibans"]  // 
          - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - Ibans: array[object]  // 
          - Type: string [example="Ibans"]  // 
          - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - CustomerConcentrationAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="a4db987a-12e0-445d-b83a-2401503dcd40"]  // 
      - SupplierConcentrationAccount: object|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /companies.info   [tags: Companies]
PAGE TEXT: Get details for a specific company.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
      - SearchKey: string [example="HORUS"]  // 
      - Name: string [example="Horus Software"]  // 
      - Name2: string|null  // 
      - Address: string [example="Quai des ardennes, 9"]  // 
      - Address2: string  // 
      - ZipCode: string [example="4020"]  // 
      - Locality: string [example="Liège"]  // 
      - CountryCode: string [example="BE"]  // 
      - IsVatLiable: boolean [example=true]  // 
      - VatNumber: string|null [example="BE0478696879"]  // Only if 'IsVatLiable' is true.
      - EnterpriseNumber: string|null  // Only if 'IsVatLiable' is false.
      - CurrencyCode: string|null  // 
      - Language: string enum["FR", "NL", "DE", "EN", "ES", "PT", "XX"] [example="FR"]  // 
      - ContactName: string|null  // 
      - ContactEmail: string|null [example="info@horus-software.be"]  // 
      - ContactPhone: string|null  // 
      - ContactWebsite: string|null [example="<https://horussoftware.be>"]  // 
      - InvoiceEmail: string [example="invoices@horus-software.be"]  // 
      - ReminderEmail: string [example="reminders@horus-software.be"]  // 
      - IsBadDebtor: boolean [example=false]  // 
      - IsCustomer: boolean [example=true]  // 
      - IsSupplier: boolean [example=false]  // 
      - IsBeneficiary: boolean [example=false]  // 
      - BeneficiaryInfo: object|null  // NULL if 'IsBeneficiary' is set to 'False'.
          - BeneficiaryType: number enum[0, 10, 20, 30, 40]  // - `0`: Undefined - `10`: Employee - `20`: Manager - `30`: Freelance - `40`: Third party
          - Inactive: boolean [example=false]  // 
          - InactiveSince: string|null  // 
          - FirstName *: string [example="John"]  // 
          - LastName *: string [example="Doe"]  // 
          - Email: string [example="john.doe@gmail.com"]  // 
          - DefaultComment: string [example="Your salary for this month"]  // 
          - DefaultSalaryAmount: number|null [example=3000]  // 
          - DefaultCurrentAccount: object|null  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="8155faa5-187c-48e8-b50b-7e815f58ff5e"]  // 
          - DefaultSalaryAccount: object|null  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="409b3629-5895-40ea-88b1-7db371a5bc32"]  // 
      - UsualCustomerPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
      - UsualSupplierPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
      - CustomerActivitySuspended: boolean [example=false]  // 
      - CustomerDomiciliationReference: string|null  // 
      - CustomerDomiciliationStartDate: string|null  // 
      - CustomerDomiciliationType: number enum[0, 1]  // - `0`: CORE - `1`: B2B
      - CustomerPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
      - SupplierPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
      - Family: string|null  // 
      - ExternalReference: string|null  // 
      - LastModifiedDate: string(date-time) [example="2021-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
      - MainIban: object|null  // 
          - Type: string [example="Ibans"]  // 
          - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - DomiciliationIban: object|null  // 
          - Type: string [example="Ibans"]  // 
          - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - Ibans: array[object]  // 
          - Type: string [example="Ibans"]  // 
          - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - CustomerConcentrationAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="a4db987a-12e0-445d-b83a-2401503dcd40"]  // 
      - SupplierConcentrationAccount: object|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /companies.new   [tags: Companies]
PAGE TEXT: Add a new company.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - SearchKey *: string [example="HORUS"]  // 
  - Name *: string [example="Horus Software"]  // 
  - Name2: string  // 
  - IsCustomer *: boolean [example=true]  // 
  - IsSupplier *: boolean [example=false]  // 
  - IsVatLiable *: boolean [example=true]  // 
  - VatNumber: string [example="BE0478696879"]  // 
  - AllowDuplicateVatNumber: boolean [example=false]  // False by default. Set to true if you want to create a company even though another one with this vat number already exists.
  - LanguageCode *: string [example="FR"]  // 
  - CountryCode *: string [example="BE"]  // 
  - Address: string [example="Quai des Ardennes 9"]  // 
  - Address2: string  // 
  - ZipCode: string [example="4020"]  // 
  - Locality: string [example="Liège"]  // 
  - PhoneNumber: string  // 
  - Website: string [example="<https://horussoftware.be>"]  // 
  - ContactPerson: string  // 
  - ContactEmail: string [example="info@horus-software.be"]  // 
  - InvoiceEmail: string [example="invoices@horus-software.be"]  // 
  - ReminderEmail: string [example="reminders@horus-software.be"]  // 
  - CustomerConcentrationAccount: string [example="400000"]  // 
  - SupplierConcentrationAccount: string [example="440000"]  // 
  - CustomerPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
  - SupplierPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
  - Family: string  // 
  - ExternalReference: string  // 
  - CustomerActivitySuspended: boolean  // 
  - CustomerDomiciliationReference: string  // 
  - CustomerDomiciliationStartDate: string  // 
  - CustomerDomiciliationType: number enum[0, 1]  // - `0`: CORE - `1`: B2B
  - UsualCustomerPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - UsualSupplierPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - Ibans: array[object]  // 
      - Iban: string [example="BE72000000001616"]  // 
      - Bic: string|null [example="BPOTBEB1"]  // Optional. It will be filled automatically if not provided.
      - IsDefault: boolean [example=true]  // Only one iban in the list shoud be set to 'True'.
      - IsDomiciliation: boolean [example=false]  // One iban at most shoud be set to 'True'.
  - IsBeneficiary: boolean [example=false]  // false by default
  - BeneficiaryInfo: object  // Information required when the 'IsBeneficiary' is set to 'True'.
      - BeneficiaryType: number enum[0, 10, 20, 30, 40]  // - `0`: Undefined - `10`: Employee - `20`: Manager - `30`: Freelance - `40`: Third party
      - FirstName *: string [example="John"]  // 
      - LastName *: string [example="Doe"]  // 
      - Email: string [example="john.doe@gmail.com"]  // 
      - DefaultComment: string [example="Your salary for this month"]  // 
      - DefaultSalaryAmount: number [example=3000]  // 
      - DefaultCurrentAccountId: string  // 
      - DefaultSalaryAccountId: string  // 
RESPONSE 200: OK -> object
  - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /companies.update   [tags: Companies]
PAGE TEXT: Update an existing company. **Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an *empty non-null* string value, its previous value will be erased.
OP DESCRIPTION: Update an existing company. **Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an _empty non-null_ string value, its previous value will be erased.
REQUEST BODY (application/json) required: object
  - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // The company to update
  - SearchKey: string [example="HORUS"]  // 
  - Name: string [example="Horus Software"]  // 
  - Name2: string  // 
  - IsCustomer: boolean [example=true]  // 
  - IsSupplier: boolean  // 
  - IsVatLiable: boolean [example=true]  // 
  - VatNumber: string [example="BE0478696879"]  // 
  - LanguageCode: string [example="FR"]  // 
  - CountryCode: string [example="BE"]  // 
  - Address: string [example="Quai des Ardennes 9"]  // 
  - Address2: string  // 
  - ZipCode: string [example="4020"]  // 
  - Locality: string [example="Liège"]  // 
  - PhoneNumber: string  // 
  - Website: string [example="<https://horussoftware.be>"]  // 
  - ContactPerson: string  // 
  - ContactEmail: string [example="info@horus-software.be"]  // 
  - InvoiceEmail: string [example="invoices@horus-software.be"]  // 
  - ReminderEmail: string [example="reminders@horus-software.be"]  // 
  - CustomerConcentrationAccount: string [example="400000"]  // 
  - SupplierConcentrationAccount: string [example="440000"]  // 
  - CustomerPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
  - SupplierPaymentDelay: string [example="30E"]  // Format (Regex) : \d{1,3}(D|J|M)?(E|e|F|f)? Format: 999 [D=days/J=jours/M=months/M=mois] [E=EndOfMonth/F=FinDeMois/e=StartOfNextMonth/f=DebutMoisSuivant]. Examples: 30E = 30 days end of month; 15e = 15th of next month; 2M = in 2 months, same day as the invoice.
  - Family: string [example="SOFTWARE"]  // 
  - ExternalReference: string  // 
  - CustomerActivitySuspended: boolean  // 
  - CustomerDomiciliationReference: string  // 
  - CustomerDomiciliationStartDate: string  // 
  - CustomerDomiciliationType: number enum[0, 1]  // - `0`: CORE - `1`: B2B
  - UsualCustomerPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - UsualSupplierPaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
RESPONSE 200: OK -> object
  - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /countries.list   [tags: Countries]
PAGE TEXT: Get a list of countries.
REQUEST BODY (application/json) required: object
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The country must match **all specified** filters in order to be included in the response.
      - CountryCodes: array[string]  // Filters on country codes using the *equals* clause
      - CountryNames: array[string]  // Filters on country names in any language, using the *equals* clause
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="dcf59788-01a9-46eb-80de-a6cd282b83a4"]  // 
      - CountryCode: string [example="BE"]  // 
      - CountryNameFr: string [example="Belgique"]  // French
      - CountryNameNl: string [example="België"]  // Dutch
      - CountryNameDe: string [example="Belgien"]  // German
      - CountryNameXx: string [example="Belgium"]  // English
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /countries.info   [tags: Countries]
PAGE TEXT: Get details for a specific country.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="dcf59788-01a9-46eb-80de-a6cd282b83a4"]  // 
      - CountryCode: string [example="BE"]  // 
      - CountryNameFr: string [example="Belgique"]  // French
      - CountryNameNl: string [example="België"]  // Dutch
      - CountryNameDe: string [example="Belgien"]  // German
      - CountryNameXx: string [example="Belgium"]  // English
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /ibans.list   [tags: Ibans]
PAGE TEXT: Get a list of ibans by company.
REQUEST BODY (application/json) required: object
  - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // Get all ibans related to a company
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="4936209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - Iban: string [example="BE68539007547034"]  // 
      - Bic: string|null  // 
      - Comment: string|null  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /ibans.info   [tags: Ibans]
PAGE TEXT: Get details for a specific iban.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="d71378b8-5cc3-4676-9b2c-544c358ae16f"]  // 
      - Iban: string [example="BE72000000001616"]  // 
      - Bic: string|null [example="BPOTBEB1"]  // 
      - Comment: string|null  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /ibans.new   [tags: Ibans]
PAGE TEXT: Add an iban to an existing company.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - CompanyId *: string [example="dkehye75-f474-4b09-a1d3-aa698e18fdhe"]  // 
  - Iban: string [example="BE72000000001616"]  // 
  - Bic: string|null [example="BPOTBEB1"]  // Optional. It will be filled automatically if not provided.
  - IsDefault: boolean [example=false]  // 'True' by default if no other IBAN is related to the company yet.
  - IsDomiciliation: boolean [example=false]  // 'False' by default.
RESPONSE 200: OK -> object
  - Id: string [example="d71378b8-5cc3-4676-9b2c-544c358ae16f"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /ibans.delete   [tags: Ibans]
PAGE TEXT: Remove an iban from an existing company.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - CompanyId *: string [example="dkehye75-f474-4b09-a1d3-aa698e18fdhe"]  // 
  - Iban *: string [example="BE72000000001616"]  // 
RESPONSE 200: OK
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /ibans.clear   [tags: Ibans]
PAGE TEXT: Remove all ibans from an existing company.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - CompanyId *: string [example="dkehye75-f474-4b09-a1d3-aa698e18fdhe"]  // 
RESPONSE 200: OK
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /vehicles.list   [tags: Vehicles]
PAGE TEXT: Get a list of vehicles by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // Get all vehicles related to a folder
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The vehicle must match **all specified** filters in order to be included in the response.
      - Types: array[number enum[0, 10, 20, 30, 40, 50]]  // Filters on the vehicles' type(s)  - `0`: Undefined - `10`: Car - `20`: Bike - `30`: Motorcycle - `40`: Truck - `50`: UtilityCar
      - FuelTypes: array[number enum[0, 10, 20, 30, 40, 44, 45, 46, 50]]  // Filters on the vehicles' fuel type(s)  - `0`: Undefined - `10`: Gasoline - `20`: Diesel - `30`: LPG - `40`: Electric - `44`: HybridDiesel - `45`: HybridBenzine - `46`: FakeHybrid - `50`: Hydrogen
      - LicensePlate: string  // Filters on the license plate
      - IncludeInactive: boolean  // *FALSE* by default
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="6586209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - Heading: string [example="FIAT 500"]  // 
      - LicensePlate: string [example="1-ABC-DEF"]  // 
      - Inactive: boolean [example=false]  // 
      - InactiveSince: string|null  // 
      - Type: number enum[0, 10, 20, 30, 40, 50] [example=10]  // - `0`: Undefined - `10`: Car - `20`: Bike - `30`: Motorcycle - `40`: Truck - `50`: UtilityCar
      - FuelType: number enum[0, 10, 20, 30, 40, 44, 45, 46, 50] [example=10]  // - `0`: Undefined - `10`: Gasoline - `20`: Diesel - `30`: LPG - `40`: Electric - `44`: HybridDiesel - `45`: HybridBenzine - `46`: FakeHybrid - `50`: Hydrogen
      - AcquisitionMode: number enum[0, 10, 20, 30, 40, 50, 60] [example=0]  // - `0`: Undefined - `10`: Purchase - `20`: FinancialLeasing - `30`: FinancialLeasingPurchaseOption - `40`: OperationalLeasing - `50`: OperationalLeasingPurchaseOption - `60`: Renting
      - AcquisitionValue: number [example=12990]  // 
      - AcquisitionDate: string(date-time) [example="2020-01-01T00:00:00+00:00"]  // 
      - FiscalValue: number [example=12990]  // 
      - CO2: number [example=120]  // 
      - FirstRegistrationDate: string(date-time) [example="2020-01-14T00:00:00+00:00"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Driver: object  // 
          - Type: string [example="Companies"]  // 
          - Id: string [example="ake897e5-f474-4b09-a1d3-aa698e18f456"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /vehicles.info   [tags: Vehicles]
PAGE TEXT: Get details for a specific vehicle.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="6586209e-dd3a-45e8-bb1c-911c8f54960b"]  // 
      - Heading: string [example="FIAT 500"]  // 
      - LicensePlate: string [example="1-ABC-DEF"]  // 
      - Inactive: boolean [example=false]  // 
      - InactiveSince: string|null  // 
      - Type: number enum[0, 10, 20, 30, 40, 50] [example=10]  // - `0`: Undefined - `10`: Car - `20`: Bike - `30`: Motorcycle - `40`: Truck - `50`: UtilityCar
      - FuelType: number enum[0, 10, 20, 30, 40, 44, 45, 46, 50] [example=10]  // - `0`: Undefined - `10`: Gasoline - `20`: Diesel - `30`: LPG - `40`: Electric - `44`: HybridDiesel - `45`: HybridBenzine - `46`: FakeHybrid - `50`: Hydrogen
      - AcquisitionMode: number enum[0, 10, 20, 30, 40, 50, 60] [example=0]  // - `0`: Undefined - `10`: Purchase - `20`: FinancialLeasing - `30`: FinancialLeasingPurchaseOption - `40`: OperationalLeasing - `50`: OperationalLeasingPurchaseOption - `60`: Renting
      - AcquisitionValue: number [example=12990]  // 
      - AcquisitionDate: string(date-time) [example="2020-01-01T00:00:00+00:00"]  // 
      - FiscalValue: number [example=12990]  // 
      - CO2: number [example=120]  // 
      - FirstRegistrationDate: string(date-time) [example="2020-01-14T00:00:00+00:00"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Driver: object  // 
          - Type: string [example="Companies"]  // 
          - Id: string [example="ake897e5-f474-4b09-a1d3-aa698e18f456"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /fiscal-years.list   [tags: Fiscal Years]
PAGE TEXT: Get a list of fiscal years by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The fiscal year must match **all specified** filters in order to be included in the response.
      - Dates: array[string]  // Filters on fiscal years encapsulating the dates
      - IncludeFuture: boolean  // *FALSE* by default
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="d5570631-54c9-44dc-831c-27d871409f58"]  // 
      - Heading: string [example="2017 - 2018"]  // 
      - StartDate: string(date-time) [example="2017-01-01T00:00:00+00:00"]  // 
      - EndDate: string(date-time) [example="2017-12-31T23:59:59+00:00"]  // 
      - LastVatClosureDate: string|null  // 
      - LastPurchasesClosureDate: string|null  // 
      - LastSalesClosureDate: string|null  // 
      - LastFinancialsClosureDate: string|null  // 
      - LastMiscOperationsClosureDate: string|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /fiscal-years.info   [tags: Fiscal Years]
PAGE TEXT: Get details for a specific fiscal year.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="df20cf3c-fb41-46f3-82f6-05e985d27fa3"]  // 
      - Heading: string [example="2018 - 2019"]  // 
      - StartDate: string(date-time) [example="2018-01-01T00:00:00+00:00"]  // 
      - EndDate: string(date-time) [example="2018-12-31T23:59:59+00:00"]  // 
      - LastVatClosureDate: string|null  // 
      - LastPurchasesClosureDate: string|null  // 
      - LastSalesClosureDate: string|null  // 
      - LastFinancialsClosureDate: string|null  // 
      - LastMiscOperationsClosureDate: string|null  // 
      - IsClosed: boolean [example=false]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /daybooks.list   [tags: Daybooks]
PAGE TEXT: Get a list of daybooks by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The daybook must match **all specified** filters in order to be included in the response.
      - SearchKey: string [example="PUR"]  // Filters on search keys
      - Heading: string [example="Purchases"]  // Filters on headings
      - Types: array[number enum[0, 100, 150, 200, 250, 500, 550, 590, 600, 610, 690, 700, 900, 990]]  // Filters on daybook's type  - `0`: Undefined - `100`: Purchase - `150`: PurchaseCreditNote - `200`: Sale - `250`: SaleCreditNote - `500`: Bank - `550`: Cash - `590`: Financial - `600`: MiscOperation - `610`: TemporaryMiscOperation - `690`: SystemMiscOperation - `700`: CostMiscOperation - `900`: Budget - `990`: External
      - Iban: string  // Filters on daybook's iban using the *equals* clause (for *Bank*, *Financial* daybooks)
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="4452b13c-3209-4e3d-94a6-ccb8a7867070"]  // 
      - SearchKey: string [example="PUR"]  // 
      - Heading: string [example="Purchases"]  // 
      - Type: number enum[0, 100, 150, 200, 250, 500, 550, 590, 600, 610, 690, 700, 900, 990] [example=100]  // - `0`: Undefined - `100`: Purchase - `150`: PurchaseCreditNote - `200`: Sale - `250`: SaleCreditNote - `500`: Bank - `550`: Cash - `590`: Financial - `600`: MiscOperation - `610`: TemporaryMiscOperation - `690`: SystemMiscOperation - `700`: CostMiscOperation - `900`: Budget - `990`: External
      - Iban: string|null  // 
      - Bic: string|null  // 
      - WithCurrency: boolean [example=false]  // Can be true only for "Bank" types
      - CurrencyCode: string|null  // 
      - IsUsed: boolean [example=true]  // 
      - IsWages: boolean [example=false]  // Can be true only for "MiscOperation" types, when the daybook is used for wages/salaries
      - ConcentrationAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="3e84fd1f-1371-414b-b666-b946348bc211"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /daybooks.info   [tags: Daybooks]
PAGE TEXT: Get details for a specific daybook.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="4452b13c-3209-4e3d-94a6-ccb8a7867070"]  // 
      - SearchKey: string [example="PUR"]  // 
      - Heading: string [example="Purchases"]  // 
      - Type: number enum[0, 100, 150, 200, 250, 500, 550, 590, 600, 610, 690, 700, 900, 990] [example=100]  // - `0`: Undefined - `100`: Purchase - `150`: PurchaseCreditNote - `200`: Sale - `250`: SaleCreditNote - `500`: Bank - `550`: Cash - `590`: Financial - `600`: MiscOperation - `610`: TemporaryMiscOperation - `690`: SystemMiscOperation - `700`: CostMiscOperation - `900`: Budget - `990`: External
      - Iban: string|null  // 
      - Bic: string|null  // 
      - WithCurrency: boolean [example=false]  // Can be true only for "Bank" types
      - CurrencyCode: string|null  // 
      - IsUsed: boolean [example=true]  // 
      - IsWages: boolean [example=false]  // Can be true only for "MiscOperation" types, when the daybook is used for wages/salaries
      - ConcentrationAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="3e84fd1f-1371-414b-b666-b946348bc211"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /daybooks.new   [tags: Daybooks]
PAGE TEXT: Add a new daybook to a folder.
REQUEST BODY (application/json) required: object
  - FolderId: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - SearchKey: string [example="PUR"]  // 
  - Heading: string [example="Purchases"]  // 
  - WithCurrency: boolean [example=false]  // Can be true only for "Bank" types
  - CurrencyCode: string|null  // 
  - Type: number enum[100, 150, 200, 250, 500, 590, 600] [example=100]  // - `100`: Purchase - `150`: PurchaseCreditNote - `200`: Sale - `250`: SaleCreditNote - `500`: Bank - `590`: Financial (= Credit card) - `600`: MiscOperation (= Miscellaneous operation)
  - ConcentrationAccountId: string|null  // Only for type "Bank" and "Financial". The id of the general financial account.
  - Iban: string|null [example="BEXXXXXXXXXXXXXX"]  // Only for type "Bank"
  - Bic: string|null  // Only for type "Bank"
  - BankName: string|null  // Only for type "Bank"
  - UsedForSupplierPayments: boolean [example=false]  // Only for type "Bank", false by default
  - UsedForClientDomiciliations: boolean [example=false]  // Only for type "Bank", false by default
  - IsWages: boolean [example=false]  // Only for type "Miscellaneous Operation" , true when the daybook is used for wages/salaries.
RESPONSE 200: OK -> object
  - Id: string [example="4452b13c-3209-4e3d-94a6-ccb8a7867070"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /daybooks.update   [tags: Daybooks]
PAGE TEXT: Update an existing daybook. **Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an *empty non-null* string value, its previous value will be erased.
OP DESCRIPTION: Update an existing daybook. **Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an _empty non-null_ string value, its previous value will be erased.
REQUEST BODY (application/json) required: object
  - DaybookId *: string [example="4452b13c-3209-4e3d-94a6-ccb8a7867070"]  // The daybook to update
  - SearchKey: string [example="PUR2"]  // Optional
  - Heading: string [example="Purchases 2"]  // Optional
RESPONSE 200: OK -> object
  - Id: string [example="4452b13c-3209-4e3d-94a6-ccb8a7867070"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /accounts.list   [tags: Accounts]
PAGE TEXT: Get a list of accounts by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The account must match **all specified** filters in order to be included in the response.
      - SearchKeys: array[string]  // Filters on search keys matching the *starts with* clause
      - Heading: string [example="Clients"]  // Filters on headings
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="1a2752b0-310d-4ef4-bc9d-a82d8807c598"]  // 
      - Inactive: boolean [example=false]  // 
      - InactiveSince: string|null  // 
      - SearchKey: string [example="400000"]  // 
      - Heading: string [example="Clients"]  // 
      - AlternateHeading: string|null  // 
      - IsSummary: boolean [example=true]  // 
      - IsInterCompany: boolean [example=false]  // 
      - IsMatchable: boolean [example=false]  // 
      - VatRate: number|null  // 
      - VatNat: number|null  // 
      - IntCategory: string|null [example="COLLECCUS"]  // Internal category
      - AccountCategory: number|null enum[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]  // - `0`: Undefined - `100`: Assets - "Compte d'actif" - `200`: FxCostPrep - "Frais de constitution immobilisés" - `300`: FxIncorp - "Immobilisés incorporels" - `400`: FxCorp - "Immobilisés corporels" - `500`: FxFinance - "Immobilisés financiers" - `600`: Liability - "Compte de passif" - `700`: Income - "Compte de produit" - `800`: DiscInc - ""Remises accordées" - `900`: Expenses - "Compte de charge" - `1000`: DiscExp - "Remises obtenues" - `1100`: Prov - "Compte de provisions" - `1200`: CostInc - "Compte analytique de produit" - `1300`: CostExp - "Compte analytique de charge"
      - AccountSubCategory: number|null enum[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1510, 1600, 1610, 1620, 2000, 2100, 2110, 2120, 2130, 2140, 2190, 2200, 2250, 2300, 2400, 2990, 3000, 3010]  // - `0`: Undefined - `100`: ADebtPlus - "Créances à plus d'un an" - `200`: AStocks - "Stock et commandes en cours" - `300`: ADebtLess - "Créances à un an au plus" - `400`: AInvest - "Placements de trésorerie" - `500`: ADispo - "Valeurs disponibles" - `600`: AAdjust - "Comptes de régularisation" - `700`: AcqVal - "Valeur d'acquisition" - `800`: SurpassAct - "Plus values actées" - `900`: WrDown - "Amortissement / réduction de valeur" - `1000`: LEquity - "Capitaux propres" - `1100`: LProv - "Provisions et impôts différés" - `1200`: LDebtPlus - "Dettes à plus d'un an" - `1300`: LDebtLess - "Dettes à un an au plus" - `1400`: LAdjust - "Comptes de régularisation" - `1500`: AReceivablePlus - "Créances à plus d'un an" - `1510`: AReceivablePlusInterest - "Créances à plus d'un an donnant lieu à intérêts" - `1600`: AReceivableLess - "Créances à un an au plus" - `1610`: AReceivableLessInterest - "Créances à un an au plus donnant lieu à intérêts" - `1620`: ACurrentAccount - "Compte courant Associé donnant lieu à intérêts" - `2000`: EGoods - "Marchandises, approvisionnement, matières premières" - `2100`: EFacility - "Frais de locaux" - `2110`: EEquipment - "Frais de matériels" - `2120`: EVehicle - "Véhicules, matériel roulant" - `2130`: EAdmin - "Frais administratif" - `2140`: ESales - "Frais commerciaux, marketing promotion et représentation" - `2190`: EOtherOverHead - "Frais généraux divers" - `2200`: EWages - "Salaires et rémunérations" - `2250`: EFreeLance - "Rémunérations intérimaires, indépendants, administrateurs ..." - `2300`: EDepreciation - "Dotation aux amortissements" - `2400`: EStock - "Réduction valeur stock" - `2990`: EOther - "Autres frais" - `3000`: ITurnOver - "Chiffre d'affaires" - `3010`: IOther - "Autres produits"
      - AccountProcessType: number|null enum[0, 10, 20, 30, 40, 50]  // - `0`: None - `10`: ToAsset - "Reclassement à l'actif si le solde débiteur" - `20`: ToLiability - "Reclassement au passif si le solde créditeur" - `30`: ToTempAsset - "Reclassement provisoire à l'actif si le solde débiteur" - `40`: ToTempLiability - "Reclassement provisoire au passif si le solde créditeur" - `50`: Automatic - "Transfert automatique"
      - DisallowedExpenseCategory: string|null  // 
      - HasPersonalShare: boolean [example=true]  // 
      - PersonalShare: number|null [example=0.2]  // 
      - PersonalShareAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="akd988d4-14e7-4ec4-bede-f03859bccdfr"]  // 
      - ProcessAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="5cc988d4-14e7-4ec4-bede-f03859bccf33"]  // 
      - DepreciationAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="8c4e1edb-6e2b-49da-82cb-af8df6c04fe2"]  // 
      - AddedValueAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="709b2171-fab7-4a2c-96ed-e36334b3f196"]  // 
      - AllowanceAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="af3de8e2-9e18-4014-9f93-6cf80ae9f7cf"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /accounts.info   [tags: Accounts]
PAGE TEXT: Get details for a specific account.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="1a2752b0-310d-4ef4-bc9d-a82d8807c598"]  // 
      - Inactive: boolean [example=false]  // 
      - InactiveSince: string|null  // 
      - SearchKey: string [example="400000"]  // 
      - Heading: string [example="Clients"]  // 
      - AlternateHeading: string|null  // 
      - IsSummary: boolean [example=true]  // 
      - IsInterCompany: boolean [example=false]  // 
      - IsMatchable: boolean [example=false]  // 
      - VatRate: number|null  // 
      - VatNat: number|null  // 
      - IntCategory: string|null [example="COLLECCUS"]  // Internal category
      - AccountCategory: number|null enum[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]  // - `0`: Undefined - `100`: Assets - "Compte d'actif" - `200`: FxCostPrep - "Frais de constitution immobilisés" - `300`: FxIncorp - "Immobilisés incorporels" - `400`: FxCorp - "Immobilisés corporels" - `500`: FxFinance - "Immobilisés financiers" - `600`: Liability - "Compte de passif" - `700`: Income - "Compte de produit" - `800`: DiscInc - ""Remises accordées" - `900`: Expenses - "Compte de charge" - `1000`: DiscExp - "Remises obtenues" - `1100`: Prov - "Compte de provisions" - `1200`: CostInc - "Compte analytique de produit" - `1300`: CostExp - "Compte analytique de charge"
      - AccountSubCategory: number|null enum[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1510, 1600, 1610, 1620, 2000, 2100, 2110, 2120, 2130, 2140, 2190, 2200, 2250, 2300, 2400, 2990, 3000, 3010]  // - `0`: Undefined - `100`: ADebtPlus - "Créances à plus d'un an" - `200`: AStocks - "Stock et commandes en cours" - `300`: ADebtLess - "Créances à un an au plus" - `400`: AInvest - "Placements de trésorerie" - `500`: ADispo - "Valeurs disponibles" - `600`: AAdjust - "Comptes de régularisation" - `700`: AcqVal - "Valeur d'acquisition" - `800`: SurpassAct - "Plus values actées" - `900`: WrDown - "Amortissement / réduction de valeur" - `1000`: LEquity - "Capitaux propres" - `1100`: LProv - "Provisions et impôts différés" - `1200`: LDebtPlus - "Dettes à plus d'un an" - `1300`: LDebtLess - "Dettes à un an au plus" - `1400`: LAdjust - "Comptes de régularisation" - `1500`: AReceivablePlus - "Créances à plus d'un an" - `1510`: AReceivablePlusInterest - "Créances à plus d'un an donnant lieu à intérêts" - `1600`: AReceivableLess - "Créances à un an au plus" - `1610`: AReceivableLessInterest - "Créances à un an au plus donnant lieu à intérêts" - `1620`: ACurrentAccount - "Compte courant Associé donnant lieu à intérêts" - `2000`: EGoods - "Marchandises, approvisionnement, matières premières" - `2100`: EFacility - "Frais de locaux" - `2110`: EEquipment - "Frais de matériels" - `2120`: EVehicle - "Véhicules, matériel roulant" - `2130`: EAdmin - "Frais administratif" - `2140`: ESales - "Frais commerciaux, marketing promotion et représentation" - `2190`: EOtherOverHead - "Frais généraux divers" - `2200`: EWages - "Salaires et rémunérations" - `2250`: EFreeLance - "Rémunérations intérimaires, indépendants, administrateurs ..." - `2300`: EDepreciation - "Dotation aux amortissements" - `2400`: EStock - "Réduction valeur stock" - `2990`: EOther - "Autres frais" - `3000`: ITurnOver - "Chiffre d'affaires" - `3010`: IOther - "Autres produits"
      - AccountProcessType: number|null enum[0, 10, 20, 30, 40, 50]  // - `0`: None - `10`: ToAsset - "Reclassement à l'actif si le solde débiteur" - `20`: ToLiability - "Reclassement au passif si le solde créditeur" - `30`: ToTempAsset - "Reclassement provisoire à l'actif si le solde débiteur" - `40`: ToTempLiability - "Reclassement provisoire au passif si le solde créditeur" - `50`: Automatic - "Transfert automatique"
      - DisallowedExpenseCategory: string|null  // 
      - HasPersonalShare: boolean [example=true]  // 
      - PersonalShare: number|null [example=0.2]  // 
      - PersonalShareAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="akd988d4-14e7-4ec4-bede-f03859bccdfr"]  // 
      - ProcessAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="5cc988d4-14e7-4ec4-bede-f03859bccf33"]  // 
      - DepreciationAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="8c4e1edb-6e2b-49da-82cb-af8df6c04fe2"]  // 
      - AddedValueAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="709b2171-fab7-4a2c-96ed-e36334b3f196"]  // 
      - AllowanceAccount: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="af3de8e2-9e18-4014-9f93-6cf80ae9f7cf"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /accounts.new   [tags: Accounts]
PAGE TEXT: Add a new account. The result will contain the generated account's id.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - SearchKey *: string [example="441000"]  // 
  - Heading *: string [example="Fournisseurs particuliers"]  // 
  - AlternateHeading: string  // Optional
  - HasPersonalShare: boolean  // Optional
  - PersonalShare: number  // Optional
RESPONSE 200: OK -> object
  - Id: string [example="djpg65d4-12e7-4ec4-bede-f03859bccpfm"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /accounts.update   [tags: Accounts]
PAGE TEXT: Update an existing account. **Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an *empty non-null* string value, its previous value will be erased.
OP DESCRIPTION: Update an existing account. **Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an _empty non-null_ string value, its previous value will be erased.
REQUEST BODY (application/json) required: object
  - AccountId *: string [example="djpg65d4-12e7-4ec4-bede-f03859bccpfm"]  // The account to update
  - Heading: string [example="Fournisseurs"]  // 
  - AlternateHeading: string  // Optional
  - HasPersonalShare: boolean  // Optional
  - PersonalShare: number  // Optional (value between 0 and 1)
RESPONSE 200: OK -> object
  - Id: string [example="djpg65d4-12e7-4ec4-bede-f03859bccpfm"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /cost-schemas.list   [tags: Cost Schemas]
PAGE TEXT: Get a list of cost schemas by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
      - OrderNo: number [example=1]  // 
      - ViewNo: number [example=0]  // 
      - SearchKey: string [example="DEPARTMENT"]  // 
      - Heading: string [example="Département"]  // 
      - AlternateHeading: string|null  // 
      - Description: string|null [example="Département interne"]  // 
      - Mandatory: boolean [example=true]  // 
      - WithReport: boolean [example=false]  // 
      - Categorized: boolean [example=false]  // 
      - CategoryHeading: string|null  // 
      - KeyLength: number [example=20]  // 
      - CostSectionType: number enum[100, 900] [example=100]  // - `100`: List - expected values are cost sections - `900`: Free - expected values are free, eventually based on a mask and a type (date, number, etc.)
      - FreeCostSectionType: number|null enum[100, 200, 300] [example="null"]  // Filled only when cost section type is 'free'  - `100`: Characters - `200`: Digits - `300`: Date
      - FreeCostSectionMask: string|null  // Filled only when cost section type is 'free'
      - VisibleInFalco: boolean [example=false]  // 
      - MasterCostSchema: object|null  // Master cost schema, can be NULL
          - Type: string [example="CostSchemas"]  // 
          - Id: string [example="e9f69608-c905-4cfe-8538-f4bd9cf4eb6d"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /cost-schemas.info   [tags: Cost Schemas]
PAGE TEXT: Get details for a specific cost schema.
REQUEST BODY (application/json) required: object
  - Id *: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
      - OrderNo: number [example=1]  // 
      - ViewNo: number [example=0]  // 
      - SearchKey: string [example="DEPARTMENT"]  // 
      - Heading: string [example="Département"]  // 
      - AlternateHeading: string|null  // 
      - Description: string|null [example="Département interne"]  // 
      - Mandatory: boolean [example=true]  // 
      - WithReport: boolean [example=false]  // 
      - Categorized: boolean [example=false]  // 
      - CategoryHeading: string|null  // 
      - KeyLength: number [example=20]  // 
      - CostSectionType: number enum[100, 900] [example=100]  // - `100`: List - expected values are cost sections - `900`: Free - expected values are free, eventually based on a mask and a type (date, number, etc.)
      - FreeCostSectionType: number|null enum[100, 200, 300] [example="null"]  // Filled only when cost section type is 'free'  - `100`: Characters - `200`: Digits - `300`: Date
      - FreeCostSectionMask: string|null  // Filled only when cost section type is 'free'
      - VisibleInFalco: boolean [example=false]  // 
      - MasterCostSchema: object|null  // Master cost schema, can be NULL
          - Type: string [example="CostSchemas"]  // 
          - Id: string [example="e9f69608-c905-4cfe-8538-f4bd9cf4eb6d"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /cost-sections.list   [tags: Cost Sections]
PAGE TEXT: Get a list of cost sections by folder and cost schema.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - CostSchemaId *: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
  - Filter: object  // *NULL* by default
      - SearchKeys: array[string]  // Filters on search keys matching the *equals* clause. Takes everything if not specified.
      - IncludeInactive: boolean [example=false]  // *FALSE* by default
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="515c66ac-7275-48c9-94bc-9a544960a0f2"]  // 
      - IsDefault: boolean [example=false]  // 
      - SearchKey: string [example="HARD"]  // 
      - Heading: string [example="Hardware"]  // 
      - AlternateHeading: string|null  // 
      - IsLocked: boolean [example=false]  // 
      - Category: string|null  // 
      - Comment: string|null  // 
      - ExtResType: string|null  // 
      - ExtResCat: string|null  // 
      - Inactive: boolean  // 
      - InactiveSince: string|null  // 
      - CostSchema: object  // 
          - Type: string [example="CostSchemas"]  // 
          - Id: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
      - MasterCostSection: object|null  // Master/parent cost section, if any
      - CostSections: array[string]  // Child cost sections, if any
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /cost-sections.info   [tags: Cost Sections]
PAGE TEXT: Get details for a specific cost section.
REQUEST BODY (application/json) required: object
  - Id *: string [example="515c66ac-7275-48c9-94bc-9a544960a0f2"]  // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="515c66ac-7275-48c9-94bc-9a544960a0f2"]  // 
      - IsDefault: boolean [example=false]  // 
      - SearchKey: string [example="HARD"]  // 
      - Heading: string [example="Hardware"]  // 
      - AlternateHeading: string|null  // 
      - IsLocked: boolean [example=false]  // 
      - Category: string|null  // 
      - Comment: string|null  // 
      - ExtResType: string|null  // 
      - ExtResCat: string|null  // 
      - Inactive: boolean  // 
      - InactiveSince: string|null  // 
      - CostSchema: object  // 
          - Type: string [example="CostSchemas"]  // 
          - Id: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
      - MasterCostSection: object|null  // Master/parent cost section, if any
      - CostSections: array[string]  // Child cost sections, if any
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /cost-sections.new   [tags: Cost Sections]
PAGE TEXT: Add a new cost section to an existing cost schema. The parent cost schema must be of type *List* (CostSectionType = 100).
The result will contain the generated cost section's id.
OP DESCRIPTION: Add a new cost section to an existing cost schema. The parent cost schema must be of type *List* (CostSectionType = 100).

The result will contain the generated cost section's id.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - CostSchemaId *: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
  - SearchKey: string [example="MYSECTION"]  // 
  - Heading: string [example="My custom section"]  // 
  - AlternateHeading: string|null  // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="ajdc66ac-7275-48c9-94bc-9a544960a0f2"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /cost-histories.list   [tags: Cost Histories]
PAGE TEXT: Get a list of cost histories by folder.
A folder can use up to **8** different cost schemas.
The response will contain a list of all defined cost schemas for the folder, with their respecting "**order no**".
It will also contain a list of all cost histories.
Every cost history can contain up to **8** cost sections.
There are 8 fields : *CostSection\<OrderNo\>*, where *\<OrderNo\>* has a value between 1 and 8.
All cost sections defined with a specific *\<OrderNo\>* are linked to the corresponding cost schema, with the same "order no".
OP DESCRIPTION: Get a list of cost histories by folder.

A folder can use up to **8** different cost schemas. 
The response will contain a list of all defined cost schemas for the folder, with their respecting "**order no**".
It will also contain a list of all cost histories.

Every cost history can contain up to **8** cost sections. 

There are 8 fields : *CostSection\<OrderNo\>*, where *\<OrderNo\>* has a value between 1 and 8. 

All cost sections defined with a specific *\<OrderNo\>* are linked to the corresponding cost schema, with the same "order no".
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - StartMonth *: number [example=1]  // 
  - StartYear *: number [example=2023]  // 
  - EndMonth *: number [example=9]  // 
  - EndYear *: number [example=2023]  // 
  - Filter: object  // *NULL* by default
      - CostSchemaIds: array[string]  // Filters on cost schemas specified by their id.
      - DaybookIds: array[string]  // Filters on daybooks specified by their id.
      - ExcludedDaybookIds: array[string]  // Filters on daybooks to exclude, specified by their id. Ignored if 'DaybookIds' was specified.
      - IncludeCompanyDetail: boolean [example=false]  // *FALSE* by default
RESPONSE 200: OK -> object
  - Data: object  // 
      - CostSchemas: array[object]  // 
          - Id: string [example="0a6d3a51-8d39-43e2-bbff-50b0175cafbc"]  // 
          - OrderNo: number [example=1]  // 
          - ViewNo: number [example=0]  // 
          - SearchKey: string [example="DEPARTMENT"]  // 
          - Heading: string [example="Département"]  // 
          - AlternateHeading: string|null  // 
          - Description: string|null [example="Département interne"]  // 
          - Mandatory: boolean [example=true]  // 
          - WithReport: boolean [example=false]  // 
          - Categorized: boolean [example=false]  // 
          - CategoryHeading: string|null  // 
          - KeyLength: number [example=20]  // 
          - CostSectionType: number enum[100, 900] [example=100]  // - `100`: List - expected values are cost sections - `900`: Free - expected values are free, eventually based on a mask and a type (date, number, etc.)
          - FreeCostSectionType: number|null enum[100, 200, 300] [example="null"]  // Filled only when cost section type is 'free'  - `100`: Characters - `200`: Digits - `300`: Date
          - FreeCostSectionMask: string|null  // Filled only when cost section type is 'free'
          - VisibleInFalco: boolean [example=false]  // 
          - MasterCostSchema: object|null  // Master cost schema, can be NULL
              - Type: string [example="CostSchemas"]  // 
              - Id: string [example="e9f69608-c905-4cfe-8538-f4bd9cf4eb6d"]  // 
          - Folder: object  // 
              - Type: string [example="Folders"]  // 
              - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - CostHistories: object  // 
          - Id: string [example="akdrk2be-8559-488a-452r-eea0dd4a7456"]  // 
          - AccountSearchKey: string [example="600000"]  // 
          - AccountHeading: string [example="Achats marchandises"]  // 
          - DaybookSearchKey: string [example="ACH"]  // 
          - DocumentNo: number [example=2301016]  // 
          - AccountingMonth: number [example=1]  // 
          - AccountingYear: number [example=2023]  // 
          - Date: string(date-time) [example="2023-01-10T00:00:00+00:00"]  // 
          - Debit: number|null [example=41.31]  // 
          - Credit: number|null  // 
          - Balance: number [example=41.31]  // 
          - Comment: string|null  // 
          - CompanyDetail: object|null  // 
              - Company: object|null  // 
                  - Type: string [example="Companies"]  // 
                  - Id: string [example="a56be925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
              - CompanySearchKey: string|null [example="MEDIA MARKT"]  // 
              - CompanyName: string|null [example="Media Markt"]  // 
          - CostSection1SearchKey: string|null [example="HARD"]  // 
          - CostSection1: object|null  // 
              - Type: string [example="CostSections"]  // 
              - Id: string [example="515c66ac-7275-48c9-94bc-9a544960a0f2"]  // 
          - CostSection2SearchKey: string|null  // 
          - CostSection2: object|null  // 
          - CostSection3SearchKey: string|null  // 
          - CostSection3: object|null  // 
          - CostSection4SearchKey: string|null  // 
          - CostSection4: object|null  // 
          - CostSection5SearchKey: string|null  // 
          - CostSection5: object|null  // 
          - CostSection6SearchKey: string|null  // 
          - CostSection6: object|null  // 
          - CostSection7SearchKey: string|null  // 
          - CostSection7: object|null  // 
          - CostSection8SearchKey: string|null  // 
          - CostSection8: object|null  // 
          - BookEntry: object  // 
              - Type: string [example="BookEntries"]  // 
              - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
          - Account: object  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="5f4g7gbe-8559-488a-b348-eea0dd4a735b"]  // 
          - Daybook: object  // 
              - Type: string [example="Daybooks"]  // 
              - Id: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
          - AccountHistory: object  // 
              - Type: string [example="AccountHistories"]  // 
              - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /account-balance.list   [tags: Account Balance]
PAGE TEXT: Get an account balance by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - StartMonth *: number [example=1]  // 
  - StartYear *: number [example=2018]  // 
  - EndMonth *: number [example=12]  // 
  - EndYear *: number [example=2018]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The account must match **all specified** filters in order to be included in the response.
      - AccountSearchKeys: array[string]  // Filters on search keys matching the *starts with* clause. Takes everything if not specified.
      - IncludeUnusedAccounts: boolean [example=true]  // *FALSE* by default. Include - or not - accounts with no movement in the selected period.
      - IncludeTitle: boolean [example=false]  // *TRUE* by default. Include - or not - titles.
      - UseAlternateHeading: boolean [example=false]  // *FALSE* by default. Use alternate heading instead of main heading.
RESPONSE 200: OK -> object
  - Data: object  // 
      - Details: array[object]  // 
          - AccountSearchKey: string [example="400000"]  // 
          - AccountHeading: string [example="Clients"]  // 
          - IsTitle: boolean [example=false]  // 
          - ReportDebit: number [example=17891.67]  // 
          - ReportCredit: number [example=0]  // 
          - PeriodDebit: number [example=46216.41]  // 
          - PeriodCredit: number [example=54410.08]  // 
          - Debit: number [example=64108.08]  // 
          - Credit: number [example=54410.08]  // 
          - IsDebitReportBalance: boolean [example=true]  // 
          - ReportBalance: number [example=17891.67]  // 
          - IsDebitPeriodBalance: boolean [example=false]  // 
          - PeriodBalance: number [example=8193.67]  // 
          - IsDebitBalance: boolean [example=true]  // 
          - Balance: number [example=9698]  // 
      - IsDebitReportBalance: boolean [example=true]  // 
      - ReportBalance: number [example=17891.67]  // 
      - IsDebitPeriodBalance: boolean [example=false]  // 
      - PeriodBalance: number [example=8193.67]  // 
      - IsDebitBalance: boolean [example=true]  // 
      - Balance: number [example=9698]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /account-histories.list   [tags: Account Histories]
PAGE TEXT: Get an account history by folder.
(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
OP DESCRIPTION: Get an account history by folder.

(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - StartMonth *: number [example=1]  // 
  - StartYear *: number [example=2018]  // 
  - EndMonth *: number [example=12]  // 
  - EndYear *: number [example=2018]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The account history must match **all specified** filters in order to be included in the response.
      - AccountSearchKeys: array[string]  // Filters on account searchkeys matching the *starts with* clause. Takes everything if not specified.
      - DaybookIds: array[string]  // Filters on daybooks specified by their id.
      - ExcludedDaybookIds: array[string]  // Filters on daybooks to exclude, specified by their id. Ignored if 'DaybookIds' was specified.
      - ExcludedEntryTypes: array[number enum[0, 100, 400, 600, 800, 810, 850, 900, 910, 1000]]  // Filters on entry types to exclude.
      - CompanyId: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // Filters on a company specified by its id.
      - BookEntryId: string  // Filters on a book entry specified by its id.
      - IncludeReport: boolean [example=true]  // *TRUE* by default
      - NotMatchedOnly: boolean [example=false]  // *FALSE* by default
      - ConfirmedOnly: boolean [example=false]  // *FALSE* by default. Include only book entries confirmed by the accountant.
      - IncludeCompanyDetail: boolean [example=false]  // *FALSE* by default
      - IncludeMatchDetail: boolean [example=false]  // *FALSE* by default
      - IncludeVatDetail: boolean [example=false]  // *FALSE* by default
      - IncludeCostDetail: boolean [example=false]  // *FALSE* by default
      - UseAlternateHeading: boolean [example=false]  // *FALSE* by default. Use alternate heading instead of main heading.
      - ModifiedAfter: string(date-time) [example="2019-01-01T00:00:00+00:00"]  // *NULL* by default. Include only account-histories modified after a given date.
      - ModifiedBefore: string(date-time) [example="2020-01-01T00:00:00+00:00"]  // *NULL* by default. Include only account-histories modified before a given date.
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
      - AccountSearchKey: string [example="400000"]  // 
      - AccountHeading: string [example="Clients"]  // 
      - DaybookSearchKey: string [example="VEN"]  // 
      - DocumentNo: number [example=1904001]  // 
      - OrderNo: number [example=1]  // 
      - AccountingMonth: number [example=4]  // 
      - AccountingYear: number [example=2019]  // 
      - Date: string(date-time) [example="2019-04-04T00:00:00+00:00"]  // 
      - DueDate: string|null  // 
      - LastModifiedDate: string(date-time) [example="2019-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
      - Debit: number|null  // 
      - Credit: number|null [example=1445.09]  // 
      - Comment: string|null  // 
      - Memo: string|null  // Only available for account statements - contains the entire communication
      - IsReport: boolean [example=false]  // 
      - AccountType: number enum[0, 100, 200, 300, 400, 500] [example=100]  // The type of the account history  - `0`: Undefined - `100`: CollectCust / Customer - `200`: CollectSup / Supplier - `300`: General - `400`: VAT - `500`: Cash
      - Confirmed: boolean [example=true]  // 
      - Verified: boolean [example=true]  // False by default. Can only ever be set to 'True' if an additionnal verification step has been configured in Horus. Contact us for more info.
      - VerifiedBy: object|null  // Nullable. Only set if 'Verified' is set to 'True'.
          - Type: string [example="Users"]  // 
          - Id: string [example="45568715-39e3-449d-a87c-8ccfcf9be53a"]  // 
      - CurrencyCode: string|null  // The currency used for this account history. *NULL* means EURO (€) was used.
      - CurrencyRate: number|null  // The currency rate used for this account history.
      - CompanyDetail: object|null  // 
          - Company: object|null  // 
              - Type: string [example="Companies"]  // 
              - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
          - CompanySearchKey: string|null [example="HORUS"]  // 
          - CompanyName: string|null [example="Horus Software"]  // 
      - VatDetail: object|null  // Only when 'IncludeVatDetail' is set to true, and folder is VAT liable.
          - VatDeclarationMonth: number|null [example=4]  // 
          - VatDeclarationYear: number|null [example=2019]  // 
          - VatRate: number|null  // 
          - VatCode: string|null  // 
          - VatHeading: string|null  // 
          - TaxType: number|null  // 0 = National, 1 = European, 2 = International
          - TaxCountryCode: string|null  // Used for OSS sales
          - TaxCondition: number|null  // *NULL* = ignore, 0 = Country, 1 = Deductibility, 2 = Investments, 3 = Percentage, 4 = Article
          - TaxConditionValue: string|null  // Only if 'TaxCondition' is set.
          - SaleTaxOrigin: number|null  // 
          - PurchaseTaxOrigin: number|null  // 
      - CostDetail: object|null  // Only when 'IncludeCostDetail' is set to true, and folder is with costs.
          - CostLines: array[object]  // 
              - OrderNo: number  // 
              - Debit: number|null  // 
              - Credit: number|null [example=1445.09]  // 
              - Costs: array[object]  // 
                  - CostSchemaSearchKey: string|null [example="DEPARTMENT"]  // 
                  - CostSchema: object|null  // 
                      - Type: string [example="CostSchemas"]  // 
                      - Id: string [example="akdrb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
                  - CostSectionSearchKey: string|null [example="IT"]  // 
                  - CostSection: object|null  // 
                      - Type: string [example="CostSections"]  // 
                      - Id: string [example="djfhre6b-0081-43f0-b398-ad81a4d79bc2"]  // 
      - MatchDetail: object|null  // 
          - MatchStatus: number enum[0, 900]  // - `0`: Partially - `900`: Totally
          - MatchNo: number|null  // 
      - Document: object|null  // 
          - Type: string [example="Documents"]  // 
          - Id: string [example="66cdb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
      - BookEntry: object|null  // 
          - Type: string [example="BookEntries"]  // 
          - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
      - Account: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="5f4g7gbe-8559-488a-b348-eea0dd4a735b"]  // 
      - Vehicle: object|null  // 
          - Type: string [example="Vehicles"]  // 
          - Id: string [example="5698efg2-8559-488a-b348-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /account-histories.info   [tags: Account Histories]
PAGE TEXT: Get details about a specific account history line, i.e. an account record line.
  param[query] Id *: string // 
  param[query] UseAlternateHeading: boolean // *FALSE* by default. Use alternate heading instead of main heading.
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
      - AccountSearchKey: string [example="400000"]  // 
      - AccountHeading: string [example="Clients"]  // 
      - DaybookSearchKey: string [example="VEN"]  // 
      - DocumentNo: number [example=1904001]  // 
      - OrderNo: number [example=1]  // 
      - AccountingMonth: number [example=4]  // 
      - AccountingYear: number [example=2019]  // 
      - Date: string(date-time) [example="2019-04-04T00:00:00+00:00"]  // 
      - DueDate: string|null  // 
      - LastModifiedDate: string(date-time) [example="2019-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
      - Debit: number|null  // 
      - Credit: number|null [example=1445.09]  // 
      - Comment: string|null  // 
      - Memo: string|null  // Only available for account statements - contains the entire communication
      - IsReport: boolean [example=false]  // 
      - AccountType: number enum[0, 100, 200, 300, 400, 500] [example=100]  // The type of the account history  - `0`: Undefined - `100`: CollectCust / Customer - `200`: CollectSup / Supplier - `300`: General - `400`: VAT - `500`: Cash
      - Confirmed: boolean [example=true]  // 
      - Verified: boolean [example=true]  // False by default. Can only ever be set to 'True' if an additionnal verification step has been configured in Horus. Contact us for more info.
      - VerifiedBy: object|null  // Nullable. Only set if 'Verified' is set to 'True'.
          - Type: string [example="Users"]  // 
          - Id: string [example="45568715-39e3-449d-a87c-8ccfcf9be53a"]  // 
      - CurrencyCode: string|null  // The currency used for this account history. *NULL* means EURO (€) was used.
      - CurrencyRate: number|null  // The currency rate used for this account history.
      - CompanyDetail: object|null  // 
          - Company: object|null  // 
              - Type: string [example="Companies"]  // 
              - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
          - CompanySearchKey: string|null [example="HORUS"]  // 
          - CompanyName: string|null [example="Horus Software"]  // 
      - VatDetail: object|null  // 
          - VatDeclarationMonth: number|null [example=4]  // 
          - VatDeclarationYear: number|null [example=2019]  // 
          - VatRate: number|null  // 
          - VatCode: string|null  // 
          - VatHeading: string|null  // 
          - TaxType: number|null  // 0 = National, 1 = European, 2 = International
          - TaxCountryCode: string|null  // Used for OSS sales
          - TaxCondition: number|null  // *NULL* = ignore, 0 = Country, 1 = Deductibility, 2 = Investments, 3 = Percentage, 4 = Article
          - TaxConditionValue: string|null  // Only if 'TaxCondition' is set.
          - SaleTaxOrigin: number|null  // 
          - PurchaseTaxOrigin: number|null  // 
      - CostDetail: object|null  // Only when folder is with costs.
          - CostLines: array[object]  // 
              - OrderNo: number  // 
              - Debit: number|null  // 
              - Credit: number|null [example=1445.09]  // 
              - Costs: array[object]  // 
                  - CostSchemaSearchKey: string|null [example="DEPARTMENT"]  // 
                  - CostSchema: object|null  // 
                      - Type: string [example="CostSchemas"]  // 
                      - Id: string [example="akdrb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
                  - CostSectionSearchKey: string|null [example="IT"]  // 
                  - CostSection: object|null  // 
                      - Type: string [example="CostSections"]  // 
                      - Id: string [example="djfhre6b-0081-43f0-b398-ad81a4d79bc2"]  // 
      - MatchDetail: object|null  // 
          - MatchStatus: number enum[0, 900]  // - `0`: Partially - `900`: Totally
          - MatchNo: number|null  // 
      - Document: object|null  // 
          - Type: string [example="Documents"]  // 
          - Id: string [example="66cdb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
      - BookEntry: object|null  // 
          - Type: string [example="BookEntries"]  // 
          - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
      - Account: object|null  // 
          - Type: string [example="Accounts"]  // 
          - Id: string [example="5f4g7gbe-8559-488a-b348-eea0dd4a735b"]  // 
      - Vehicle: object|null  // 
          - Type: string [example="Vehicles"]  // 
          - Id: string [example="5698efg2-8559-488a-b348-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.list   [tags: Book entries]
PAGE TEXT: Get a list of book entries by folder and daybook, for a given period.
(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
OP DESCRIPTION: Get a list of book entries by folder and daybook, for a given period.

(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - StartMonth *: number [example=1]  // 
  - StartYear *: number [example=2019]  // 
  - EndMonth *: number [example=12]  // 
  - EndYear *: number [example=2019]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The book entry must match **all specified** filters in order to be included in the response.
      - CompanyId: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
      - DocumentNo: number [example=1904001]  // 
      - EntryTypes: array[number enum[0, 100, 400, 600, 800, 810, 850, 900, 910, 1000]]  // 
      - ConfirmedOnly: boolean [example=false]  // *FALSE* by default. Include only book entries confirmed by the accountant.
      - ModifiedAfter: string(date-time) [example="2019-01-01T00:00:00+00:00"]  // *NULL* by default. Include only account-histories modified after a given date.
      - ModifiedBefore: string(date-time) [example="2020-01-01T00:00:00+00:00"]  // *NULL* by default. Include only account-histories modified before a given date.
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
      - DocumentNo: number [example=1904001]  // 
      - Confirmed: boolean [example=true]  // 
      - Verified: boolean [example=true]  // False by default. Can only ever be set to 'True' if an additionnal verification step has been configured in Horus. Contact us for more info.
      - VerifiedBy: object|null  // Nullable. Only set if 'Verified' is set to 'True'.
          - Type: string [example="Users"]  // 
          - Id: string [example="45568715-39e3-449d-a87c-8ccfcf9be53a"]  // 
      - EntryType: number enum[0, 100, 400, 600, 800, 810, 850, 900, 910, 1000] [example=100]  // - `0`: Undefined - `100`: Normal - `400`: ManualMO - `600`: AutomaticMO - `800`: TemporaryClosingMO - `810`: AutomaticClosingMO - `850`: FiscalClosingMO - `900`: ResultReportMO - `910`: OpeningMO - `1000`: CostMO
      - OperationType: number enum[0, 100, 200, 300] [example=0]  // - `0`: Undefined - `100`: Vat - `200`: Reclassification - `300`: Depreciation
      - Date: string(date-time) [example="2019-04-04T00:00:00+00:00"]  // 
      - LastModifiedDate: string(date-time) [example="2019-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
      - CompanyDetail: object|null  // 
          - Company: object|null  // 
              - Type: string [example="Companies"]  // 
              - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
          - RemarkPayment: string|null  // 
          - RemarkCompany: string|null  // 
          - DueDate: string|null  // 
          - PaymentDate: string|null  // 
          - TotalAmount: number|null  // 
          - TurnoverAmount: number|null  // 
          - TaxAmount: number|null  // 
          - DiscountDetail: object|null  // 
              - DiscountDate: string|null  // 
              - DiscountAmount: number|null  // 
              - DiscountRate: number|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Daybook: object  // 
          - Type: string [example="Daybooks"]  // 
          - Id: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
      - Document: object|null  // 
          - Type: string [example="Documents"]  // 
          - Id: string [example="66cdb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
      - AccountHistories: array[object]  // 
          - Type: string [example="AccountHistories"]  // 
          - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.documents.new   [tags: Book entries]
PAGE TEXT: Attach a document to an existing book entry that doesn't have any document yet. The result will contain the generated document's id.
Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
Supported document types :
- Pdf
- Xml
- CODA
- SODA
- Images (.jpg, .jpeg, .png)
**The request will fail if a document is already attached to the book entry**. In that case, use the endpoint 'book-entries.documents.annexes.new'.
OP DESCRIPTION: Attach a document to an existing book entry that doesn't have any document yet. The result will contain the generated document's id.

Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

Supported document types :
- Pdf
- Xml
- CODA
- SODA
- Images (.jpg, .jpeg, .png)

**The request will fail if a document is already attached to the book entry**. In that case, use the endpoint 'book-entries.documents.annexes.new'.
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="e5g26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - FileName *: string [example="my-invoice.pdf"]  // Required. Include the file's extension.
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="djrjz2be-8559-488a-b348-eeaqld4a548b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.documents.annexes.new   [tags: Book entries]
PAGE TEXT: Attach additional documents to an existing book entry that already has a main document. The result will contain the generated annexed document's id.
Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
Supported document types :
- Pdf
- Xml
- CODA
- SODA
- Images (.jpg, .jpeg, .png)
**The request will fail if no main document is attached to the book entry yet**. In that case, use the endpoint 'book-entries.documents.new'.
OP DESCRIPTION: Attach additional documents to an existing book entry that already has a main document. The result will contain the generated annexed document's id.

Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

Supported document types :
- Pdf
- Xml
- CODA
- SODA
- Images (.jpg, .jpeg, .png)

**The request will fail if no main document is attached to the book entry yet**. In that case, use the endpoint 'book-entries.documents.new'.
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="e5g26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - FileName *: string [example="my-invoice.pdf"]  // Required. Include the file's extension.
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="djrjz2be-8559-488a-b348-eeaqld4a548b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.miscellaneous-operations.new   [tags: Book entries]
PAGE TEXT: Insert a miscellaneous operation (OD). The result will contain the generated book entry's id.
There are two ways to insert it, either with or without an attached document.
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
The sum of the debit amount and credit amount must be balanced.
OP DESCRIPTION: Insert a miscellaneous operation (OD). The result will contain the generated book entry's id.

There are two ways to insert it, either with or without an attached document.
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

The sum of the debit amount and credit amount must be balanced.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Number *: number [example=201909001]  // The number of the miscellaneous operation, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - Confirmed: boolean [example=false]  // Nullable, *false* by default
  - AutoGenerateNumber: boolean [example=false]  // Nullable, *false* by default. Only works if "Confirmed" is set to *true*. In that case, the "Number" value will be ignored and should be left at 0. The number will be automatically generated.
  - FileName: string|null [example="my-misc-op.pdf"]  // Required if a document is attached. Include the file's extension.
  - Lines *: array[object]  // 
      - Type *: number [example=3]  // 1 for customer, 2 for supplier, 3 for general
      - Account *: string [example="499000"]  // The account's search key
      - Debit *: number [example=1000]  // Non-negative amount
      - Credit *: number [example=0]  // Non-negative amount
      - Comment: string|null [example="my comment"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId: string  // Required if type = 1 or type = 2
      - VehicleId: string|null  // Nullable. If one is provided, the corresponding vehicle will be associated to the account history, but only if the account requires it.
      - CostDistributionKey: string|null  // A cost distribution key as defined in Horus Office. When using a cost ditribution key, no cost lines must be specified. Cost lines will be used instead of cost distribution key if both are specified in the request.
      - CostLines: array[object]  // 
          - Amount *: number [example=1000]  // The sum of all cost lines' amounts must be equal to the corresponding line's debit/credit amount.
          - Costs *: array[object]  // 
              - SchemaSearchKey *: string [example="DEPARTMENT"]  // The search key of an existing cost schema.
              - Value *: string [example="OFFICE"]  // The search key of an existing cost section, linked to this cost schema
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.miscellaneous-operations.update   [tags: Book entries]
PAGE TEXT: Update a previously inserted miscellaneous operation (OD). The result will contain the **newly** generated book entry's id.
There are two ways to update it, either with or without an attached document (the original attachment will be deleted in both cases).
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
The sum of the debit amount and credit amount must be balanced.
OP DESCRIPTION: Update a previously inserted miscellaneous operation (OD). The result will contain the **newly** generated book entry's id.

There are two ways to update it, either with or without an attached document (the original attachment will be deleted in both cases).
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

The sum of the debit amount and credit amount must be balanced.
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // The id of the book entry to update
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Number *: number [example=201909001]  // The number of the miscellaneous operation, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - Confirmed: boolean [example=false]  // Nullable, *false* by default
  - AutoGenerateNumber: boolean [example=false]  // Nullable, *false* by default. Only works if "Confirmed" is set to *true*. In that case, the "Number" value will be ignored and should be left at 0. The number will be automatically generated.
  - FileName: string|null [example="my-misc-op.pdf"]  // Required if a document is attached. Include the file's extension.
  - Lines *: array[object]  // 
      - Type *: number [example=3]  // 1 for customer, 2 for supplier, 3 for general
      - Account *: string [example="499000"]  // The account's search key
      - Debit *: number [example=1000]  // Non-negative amount
      - Credit *: number [example=0]  // Non-negative amount
      - Comment: string|null [example="my new comment"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId: string  // Required if type = 1 or type = 2
      - CostDistributionKey: string|null  // A cost distribution key as defined in Horus Office. When using a cost ditribution key, no cost lines must be specified. Cost lines will be used instead of cost distribution key if both are specified in the request.
      - CostLines: array[object]  // 
          - Amount *: number [example=1000]  // The sum of all cost lines' amounts must be equal to the corresponding line's debit/credit amount.
          - Costs *: array[object]  // 
              - SchemaSearchKey *: string [example="DEPARTMENT"]  // The search key of an existing cost schema.
              - Value *: string [example="OFFICE"]  // The search key of an existing cost section, linked to this cost schema
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="azk822be-8559-488a-b348-eeaqld4dju45"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.miscellaneous-operations.lines.update   [tags: Book entries]
PAGE TEXT: Update only **one or several lines** of a previously inserted miscellaneous operation (OD). The result will contain the book entry's id.
The update doesn't allow the modification of the debit and credit amount.
**Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an *empty non-null* string value, its previous value will be erased.
OP DESCRIPTION: Update only **one or several lines** of a previously inserted miscellaneous operation (OD). The result will contain the book entry's id.

The update doesn't allow the modification of the debit and credit amount.

**Provide only the fields you want to update, or leave their value to *NULL* !** If any field is provided with an _empty non-null_ string value, its previous value will be erased.
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // The id of the book entry to update
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Lines *: array[object]  // 
      - AccountHistoryId *: string [example="09B81C9F-3B5E-EF11-874B-009337BD8E44"]  // 
      - Type: number [example=3]  // 1 for customer, 2 for supplier, 3 for general
      - Account: string [example="499000"]  // The account's search key
      - Comment: string|null [example="my new comment"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId: string  // 
RESPONSE 200: OK -> object
  - Id: string [example="azk822be-8559-488a-b348-eeaqld4dju45"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## DELETE /book-entries.miscellaneous-operations.delete   [tags: Book entries]
PAGE TEXT: Delete a previously inserted miscellaneous operation (OD).
The book entry must be non-confirmed, and have been injected through the API.
OP DESCRIPTION: Delete a previously inserted miscellaneous operation (OD). 

The book entry must be non-confirmed, and have been injected through the API.
  param[query] Id *: string // The id of the book entry to delete
RESPONSE 200: OK -> object
  - Id: string [example="azk822be-8559-488a-b348-eeaqld4dju45"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.banks.new   [tags: Book entries]
PAGE TEXT: Insert a bank operation. The result will contain the generated book entry's id.
There are two ways to insert it, either with or without an attached document.
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
OP DESCRIPTION: Insert a bank operation. The result will contain the generated book entry's id.

There are two ways to insert it, either with or without an attached document.
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // Must be of type Bank (= 500)
  - Number *: number [example=202211001]  // The number of the bank operation, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2022-11-04T00:00:00+00:00"]  // 
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - AutoGenerateNumber: boolean [example=false]  // Nullable, *false* by default. Only works if "Confirmed" is set to *true*. In that case, the "Number" value will be ignored and should be left at 0. The number will be automatically generated.
  - FileName: string|null [example="my-coda.cod"]  // Required if a document is attached. Include the file's extension.
  - Lines *: array[object]  // 
      - Type *: number [example=1]  // 1 for customer, 2 for supplier, 3 for general
      - Account *: string [example="400000"]  // The account's search key
      - Amount *: number [example=1210]  // The amount of the movement. **The eventual tax amount must be included**.
      - Comment: string|null [example="my comment"]  // 
      - Memo: string|null [example="my detailed memo comment"]  // 
      - Date *: string(date-time) [example="2022-11-04T00:00:00+00:00"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // Required if type = 1 or type = 2
      - Tax: object  // Nullable, can only be specified for lines of type 3 (= General)
          - BaseAmount: number [example=1000]  // Nullable, will be inferred from line amount and tax rate if none is provided.
          - TaxRate *: number [example=21]  // 
          - TaxAmount: number [example=210]  // Nullable, will be inferred from base amount and tax rate if none is provided.
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.banks.update   [tags: Book entries]
PAGE TEXT: Update a previously inserted financial operation. The result will contain the **newly** generated book entry's id.
There are two ways to update it, either with or without an attached document (the original attachment will be deleted in both cases).
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
OP DESCRIPTION: Update a previously inserted financial operation. The result will contain the **newly** generated book entry's id.

There are two ways to update it, either with or without an attached document (the original attachment will be deleted in both cases).
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // The id of the book entry to update
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // Must be of type Bank (= 500)
  - Number *: number [example=202211001]  // The number of the financial operation, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2022-11-04T00:00:00+00:00"]  // 
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - AutoGenerateNumber: boolean [example=false]  // Nullable, *false* by default. Only works if "Confirmed" is set to *true*. In that case, the "Number" value will be ignored and should be left at 0. The number will be automatically generated.
  - FileName: string|null [example="my-coda.cod"]  // Required if a document is attached. Include the file's extension.
  - Lines *: array[object]  // 
      - Type *: number [example=1]  // 1 for customer, 2 for supplier, 3 for general
      - Account *: string [example="400000"]  // The account's search key
      - Amount *: number [example=1210]  // 
      - Comment: string|null [example="my comment"]  // 
      - Memo: string|null [example="my detailed memo comment"]  // 
      - Date *: string(date-time) [example="2022-11-04T00:00:00+00:00"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // Required if type = 1 or type = 2
      - Tax: object  // Nullable, can only be specified for lines of type 3 (= General)
          - BaseAmount: number [example=1000]  // Nullable, will be inferred from line amount and tax rate if none is provided.
          - TaxRate *: number [example=21]  // 
          - TaxAmount: number [example=210]  // Nullable, will be inferred from base amount and tax rate if none is provided.
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="azk822be-8559-488a-b348-eeaqld4dju45"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.financials.new   [tags: Book entries]
PAGE TEXT: Insert a financial operation. The result will contain the generated book entry's id.
There are two ways to insert it, either with or without an attached document.
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
OP DESCRIPTION: Insert a financial operation. The result will contain the generated book entry's id.

There are two ways to insert it, either with or without an attached document.
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Number *: number [example=201909001]  // The number of the financial operation, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - AutoGenerateNumber: boolean [example=false]  // Nullable, *false* by default. Only works if "Confirmed" is set to *true*. In that case, the "Number" value will be ignored and should be left at 0. The number will be automatically generated.
  - FileName: string|null [example="my-financial-op.pdf"]  // Required if a document is attached. Include the file's extension.
  - Lines *: array[object]  // 
      - Type *: number [example=1]  // 1 for customer, 2 for supplier, 3 for general
      - Account *: string [example="499000"]  // The account's search key
      - Amount *: number [example=1000]  // 
      - Comment: string|null [example="my comment"]  // 
      - Memo: string|null [example="my detailed memo comment"]  // 
      - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // Required if type = 1 or type = 2
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /book-entries.financials.update   [tags: Book entries]
PAGE TEXT: Update a previously inserted financial operation. The result will contain the **newly** generated book entry's id.
There are two ways to update it, either with or without an attached document (the original attachment will be deleted in both cases).
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
OP DESCRIPTION: Update a previously inserted financial operation. The result will contain the **newly** generated book entry's id.

There are two ways to update it, either with or without an attached document (the original attachment will be deleted in both cases).
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the entry, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // The id of the book entry to update
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Number *: number [example=201909001]  // The number of the financial operation, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - AutoGenerateNumber: boolean [example=false]  // Nullable, *false* by default. Only works if "Confirmed" is set to *true*. In that case, the "Number" value will be ignored and should be left at 0. The number will be automatically generated.
  - FileName: string|null [example="my-financial-op.pdf"]  // Required if a document is attached. Include the file's extension.
  - Lines *: array[object]  // 
      - Type *: number [example=1]  // 1 for customer, 2 for supplier, 3 for general
      - Account *: string [example="499000"]  // The account's search key
      - Amount *: number [example=1000]  // 
      - Comment: string|null [example="my comment"]  // 
      - Memo: string|null [example="my detailed memo comment"]  // 
      - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
      - MatchNo: number|null  // *NULL* By default.
      - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // Required if type = 1 or type = 2
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="azk822be-8559-488a-b348-eeaqld4dju45"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /customers.outstanding   [tags: Customers]
PAGE TEXT: Get a customer's outstanding debts.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // 
      - CompanyIds: array[string]  // Filters on companies specified by their id.
      - IncludeVatDetail: boolean [example=false]  // *FALSE* by default
      - UseAlternateHeading: boolean [example=false]  // *FALSE* by default. Use alternate heading instead of main heading.
RESPONSE 200: OK -> object
  - Data: object  // 
      - SumDebit: number [example=0]  // 
      - SumCredit: number [example=1445.09]  // 
      - AccountHistories: array[object]  // 
          - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
          - AccountSearchKey: string [example="400000"]  // 
          - AccountHeading: string [example="Clients"]  // 
          - DaybookSearchKey: string [example="VEN"]  // 
          - DocumentNo: number [example=1904001]  // 
          - OrderNo: number [example=1]  // 
          - AccountingMonth: number [example=4]  // 
          - AccountingYear: number [example=2019]  // 
          - Date: string(date-time) [example="2019-04-04T00:00:00+00:00"]  // 
          - DueDate: string|null  // 
          - LastModifiedDate: string(date-time) [example="2019-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
          - Debit: number|null  // 
          - Credit: number|null [example=1445.09]  // 
          - ReminderLevel: number|null [example=1]  // 
          - Comment: string|null  // 
          - Memo: string|null  // Only available for account statements - contains the entire communication
          - IsReport: boolean [example=false]  // 
          - AccountType: number enum[0, 100, 200, 300, 400, 500] [example=100]  // The type of the account history  - `0`: Undefined - `100`: CollectCust / Customer - `200`: CollectSup / Supplier - `300`: General - `400`: VAT - `500`: Cash
          - Confirmed: boolean [example=true]  // 
          - CurrencyCode: string|null  // The currency used for this account history. *NULL* means EURO (€) was used.
          - CurrencyRate: number|null  // The currency rate used for this account history.
          - CompanyDetail: object|null  // 
              - Company: object|null  // 
                  - Type: string [example="Companies"]  // 
                  - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
              - CompanySearchKey: string|null [example="HORUS"]  // 
              - CompanyName: string|null [example="Horus Software"]  // 
          - VatDetail: object|null  // 
              - VatDeclarationMonth: number|null [example=4]  // 
              - VatDeclarationYear: number|null [example=2019]  // 
              - VatRate: number|null  // 
              - VatCode: string|null  // 
              - VatHeading: string|null  // 
              - TaxType: number|null  // 0 = National, 1 = European, 2 = International
              - TaxCountryCode: string|null  // Used for OSS sales
              - SaleTaxOrigin: number|null  // 
              - PurchaseTaxOrigin: number|null  // 
          - MatchDetail: object|null  // 
              - MatchStatus: number enum[0, 900]  // - `0`: Partially - `900`: Totally
              - MatchNo: number|null  // 
          - Document: object|null  // 
              - Type: string [example="Documents"]  // 
              - Id: string [example="66cdb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
          - BookEntry: object|null  // 
              - Type: string [example="BookEntries"]  // 
              - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
          - Account: object|null  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="5f4g7gbe-8559-488a-b348-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /suppliers.outstanding   [tags: Suppliers]
PAGE TEXT: Get a supplier's outstanding debts.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // 
      - CompanyIds: array[string]  // Filters on companies specified by their id.
      - IncludeVatDetail: boolean [example=false]  // *FALSE* by default
      - UseAlternateHeading: boolean [example=false]  // *FALSE* by default. Use alternate heading instead of main heading.
RESPONSE 200: OK -> object
  - Data: object  // 
      - SumDebit: number [example=1445.09]  // 
      - SumCredit: number [example=0]  // 
      - AccountHistories: array[object]  // 
          - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
          - AccountSearchKey: string [example="440000"]  // 
          - AccountHeading: string [example="Fournisseurs"]  // 
          - DaybookSearchKey: string [example="ACH"]  // 
          - DocumentNo: number [example=1904001]  // 
          - OrderNo: number [example=1]  // 
          - AccountingMonth: number [example=4]  // 
          - AccountingYear: number [example=2019]  // 
          - Date: string(date-time) [example="2019-04-04T00:00:00+00:00"]  // 
          - DueDate: string|null  // 
          - LastModifiedDate: string(date-time) [example="2019-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
          - Debit: number|null [example=1445.09]  // 
          - Credit: number|null  // 
          - Comment: string|null  // 
          - Memo: string|null  // Only available for account statements - contains the entire communication
          - IsReport: boolean [example=false]  // 
          - AccountType: number enum[0, 100, 200, 300, 400, 500] [example=100]  // The type of the account history  - `0`: Undefined - `100`: CollectCust / Customer - `200`: CollectSup / Supplier - `300`: General - `400`: VAT - `500`: Cash
          - Confirmed: boolean [example=true]  // 
          - CurrencyCode: string|null  // The currency used for this account history. *NULL* means EURO (€) was used.
          - CurrencyRate: number|null  // The currency rate used for this account history.
          - CompanyDetail: object|null  // 
              - Company: object|null  // 
                  - Type: string [example="Companies"]  // 
                  - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
              - CompanySearchKey: string|null [example="HORUS"]  // 
              - CompanyName: string|null [example="Horus Software"]  // 
          - VatDetail: object|null  // 
              - VatDeclarationMonth: number|null [example=4]  // 
              - VatDeclarationYear: number|null [example=2019]  // 
              - VatRate: number|null  // 
              - VatCode: string|null  // 
              - VatHeading: string|null  // 
              - TaxType: number|null  // 0 = National, 1 = European, 2 = International
              - TaxCountryCode: string|null  // Used for OSS sales
              - SaleTaxOrigin: number|null  // 
              - PurchaseTaxOrigin: number|null  // 
          - MatchDetail: object|null  // 
              - MatchStatus: number enum[0, 900]  // - `0`: Partially - `900`: Totally
              - MatchNo: number|null  // 
          - Document: object|null  // 
              - Type: string [example="Documents"]  // 
              - Id: string [example="66cdb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
          - BookEntry: object|null  // 
              - Type: string [example="BookEntries"]  // 
              - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
          - Account: object|null  // 
              - Type: string [example="Accounts"]  // 
              - Id: string [example="5f4g7gbe-8559-488a-b348-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /documents.list   [tags: Documents]
PAGE TEXT: Get a list of documents by folder, created between dates.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - CreatedBefore *: string(date-time) [example="2022-01-01T00:00:00+00:00"]  // 
  - CreatedAfter *: string(date-time) [example="2021-10-01T00:00:00+00:00"]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The document must match **all specified** filters in order to be included in the response.
      - Types: array[number enum[0, 100, 210, 220, 300, 310, 400, 410, 420, 500, 600, 901, 1000, 9000, 10000, 10100, 10120, 10130, 10140, 10200]]  // Filters on the documents' type(s)  - `0`: Unknown - `100`: ExpenseAccount - `210`: PurchaseInvoice - `220`: PurchaseCreditNote - `300`: SaleInvoice - `310`: SaleCreditNote - `400`: BankStatement - `410`: CreditCardStatement - `420`: CashStatement - `500`: VatAcknowledge - `600`: MiscellaneousOperation - `901`: Duplicata - `1000`: OtherDocument - `9000`: MessageAttachment - `10000`: Library - `10100`: AdminDocument - `10120`: VatStatement - `10130`: SocialStatement - `10140`: SalaryStatement - `10200`: OfficialDocument
      - Status: array[number enum[0, 100, 200, 300, 301, 400, 500, 600, 700, 800, 900, 901, 1000, 1100, 1200]]  // Filters on the documents' status (array of status)  - `0`: Undefined - `100`: WaitingConfirmation - `200`: Confirmed - `300`: WaitingPostProcessing - `301`: BeingPostProcessed - `400`: BeingProcessed - `500`: ProcessingFailed - `600`: Deleted - `700`: WaitingCut - `800`: Temporary - `900`: PossibleDuplicata - `901`: DuplicataNumber - `1000`: Invalid - `1100`: WrongFolder - `1200`: Anomaly
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="00997d06-c062-4681-a794-b7c22381642b"]  // 
      - CreationDate: string(date-time) [example="2021-11-23T00:00:00+00:00"]  // 
      - Type: number enum[0, 100, 210, 220, 300, 310, 400, 410, 420, 500, 600, 901, 1000, 9000, 10000, 10100, 10120, 10130, 10140, 10200] [example=400]  // - `0`: Unknown - `100`: ExpenseAccount - `210`: PurchaseInvoice - `220`: PurchaseCreditNote - `300`: SaleInvoice - `310`: SaleCreditNote - `400`: BankStatement - `410`: CreditCardStatement - `420`: CashStatement - `500`: VatAcknowledge - `600`: MiscellaneousOperation - `901`: Duplicata - `1000`: OtherDocument - `9000`: MessageAttachment - `10000`: Library - `10100`: AdminDocument - `10120`: VatStatement - `10130`: SocialStatement - `10140`: SalaryStatement - `10200`: OfficialDocument
      - Status: number enum[0, 100, 200, 300, 301, 400, 500, 600, 700, 800, 900, 901, 1000, 1100, 1200] [example=100]  // - `0`: Undefined - `100`: WaitingConfirmation - `200`: Confirmed - `300`: WaitingPostProcessing - `301`: BeingPostProcessed - `400`: BeingProcessed - `500`: ProcessingFailed - `600`: Deleted - `700`: WaitingCut - `800`: Temporary - `900`: PossibleDuplicata - `901`: DuplicataNumber - `1000`: Invalid - `1100`: WrongFolder - `1200`: Anomaly
      - Confirmed: boolean [example=true]  // 
      - OriginalFileName: string [example="2021.11.01.be2xxxx20xxxx620-eur.cod"]  // 
      - UserComment: string|null  // 
      - Remark: string|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - BookEntry: object|null  // 
          - Type: string [example="BookEntries"]  // 
          - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /documents.info   [tags: Documents]
PAGE TEXT: Get details for a specific document.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="00997d06-c062-4681-a794-b7c22381642b"]  // 
      - CreationDate: string(date-time) [example="2021-11-23T00:00:00+00:00"]  // 
      - Type: number enum[0, 100, 210, 220, 300, 310, 400, 410, 420, 500, 600, 901, 1000, 9000, 10000, 10100, 10120, 10130, 10140, 10200] [example=400]  // - `0`: Unknown - `100`: ExpenseAccount - `210`: PurchaseInvoice - `220`: PurchaseCreditNote - `300`: SaleInvoice - `310`: SaleCreditNote - `400`: BankStatement - `410`: CreditCardStatement - `420`: CashStatement - `500`: VatAcknowledge - `600`: MiscellaneousOperation - `901`: Duplicata - `1000`: OtherDocument - `9000`: MessageAttachment - `10000`: Library - `10100`: AdminDocument - `10120`: VatStatement - `10130`: SocialStatement - `10140`: SalaryStatement - `10200`: OfficialDocument
      - Status: number enum[0, 100, 200, 300, 301, 400, 500, 600, 700, 800, 900, 901, 1000, 1100, 1200] [example=100]  // - `0`: Undefined - `100`: WaitingConfirmation - `200`: Confirmed - `300`: WaitingPostProcessing - `301`: BeingPostProcessed - `400`: BeingProcessed - `500`: ProcessingFailed - `600`: Deleted - `700`: WaitingCut - `800`: Temporary - `900`: PossibleDuplicata - `901`: DuplicataNumber - `1000`: Invalid - `1100`: WrongFolder - `1200`: Anomaly
      - Confirmed: boolean [example=true]  // 
      - OriginalFileName: string [example="2021.11.01.be2xxxx20xxxx620-eur.cod"]  // 
      - UserComment: string|null  // 
      - Remark: string|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - BookEntry: object|null  // 
          - Type: string [example="BookEntries"]  // 
          - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /documents.download   [tags: Documents]
PAGE TEXT: Download the bytes for a specific document.
  param[query] Id *: string // 
RESPONSE 200: The file's bytes. -> string(binary)
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /documents.new   [tags: Documents]
PAGE TEXT: Insert a document, which will be processed automatically and transformed into a book entry. The result will contain the generated document's id.
Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
Supported document types :
- Pdf
- Xml
- CODA
- SODA
- Images (.jpg, .jpeg, .png)
OP DESCRIPTION: Insert a document, which will be processed automatically and transformed into a book entry. The result will contain the generated document's id.

Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

Supported document types :
- Pdf
- Xml
- CODA
- SODA
- Images (.jpg, .jpeg, .png)
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - FileName *: string [example="my-invoice.pdf"]  // Required. Include the file's extension.
  - UserComment: string|null [example="my client comment"]  // 
  - Remark: string|null [example="Invoice 230601"]  // 
  - VehicleId: string|null  // Give info about the related vehicle
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0dajz2be-8559-488a-b348-eeaqld4a548b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /library.documents.list   [tags: Library Documents]
PAGE TEXT: Get a list of library documents by folder.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. The document must match **all specified** filters in order to be included in the response.
      - CreatedBefore: string(date-time) [example="2022-10-01T00:00:00+00:00"]  // 
      - CreatedAfter: string(date-time) [example="2021-10-01T00:00:00+00:00"]  // 
      - Categories: array[string]  // Filters on the library documents' category(ies). Below you can find all categories existing by default. If needed, you can also specify a custom one.  - `Undefined`: Undefined - `Vat`: VAT document - `Admin`: Admin document - `Social`: Social document - `AccountReport`: Accounting report - `Bank`: Bank document - `PermanentFolder`: Accountant folder - `Others`: Others - `<AnyOtherCustomCategoryName>`: Custom category name
      - Title: string [example="my document"]  // Filters on library documents' titles containing (at least) one of the words provided.
      - Search: string [example="my description"]  // Filters on library documents' titles/descriptions/key words containing (at least) one of the words provided.
      - ReferenceDateStartMonth: number  // 
      - ReferenceDateStartYear: number  // 
      - ReferenceDateEndMonth: number  // 
      - ReferenceDateEndYear: number  // 
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - Id: string [example="akey7d06-c062-4681-a794-b7c22381dkr5"]  // 
      - CreationDate: string(date-time) [example="2022-08-23T00:00:00+00:00"]  // 
      - Title: string [example="my document"]  // 
      - Category: string [example="Admin"]  // 
      - FileName: string [example="myDocument.pdf"]  // 
      - Comment: string|null [example="here is my description."]  // 
      - KeyWords: array[string]  // 
      - ReferenceDateMonth: number [example=8]  // 
      - ReferenceDateYear: number [example=2022]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /library.documents.info   [tags: Library Documents]
PAGE TEXT: Get details for a specific library document.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="akey7d06-c062-4681-a794-b7c22381dkr5"]  // 
      - CreationDate: string(date-time) [example="2022-08-23T00:00:00+00:00"]  // 
      - Title: string [example="my document"]  // 
      - Category: string enum["Undefined", "Vat", "Admin", "Social", "AccountReport", "Bank", "PermanentFolder", "Others", "<AnyOtherCustomCategoryName>"] [example="Admin"]  // - `Undefined`: Undefined - `Vat`: VAT document - `Admin`: Admin document - `Social`: Social document - `AccountReport`: Accounting report - `Bank`: Bank document - `PermanentFolder`: Accountant folder - `Others`: Others - `<AnyOtherCustomCategoryName>`: Custom category name
      - FileName: string [example="myDocument.pdf"]  // 
      - Comment: string|null [example="here is my description."]  // 
      - KeyWords: array[string]  // 
      - ReferenceDateMonth: number [example=8]  // 
      - ReferenceDateYear: number [example=2022]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /library.documents.download   [tags: Library Documents]
PAGE TEXT: Download the bytes for a specific library document.
  param[query] Id *: string // 
RESPONSE 200: The file's bytes. -> string(binary)
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /library.documents.new   [tags: Library Documents]
PAGE TEXT: Insert a document into the library. The result will contain the generated document's id.
Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
OP DESCRIPTION: Insert a document into the library. The result will contain the generated document's id.

Use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Title: string [example="my document"]  // 
  - Category: string enum["Undefined", "Vat", "Admin", "Social", "AccountReport", "Bank", "PermanentFolder", "Others", "<AnyOtherCustomCategoryName>"] [example="Admin"]  // - `Undefined`: Undefined - `Vat`: VAT document - `Admin`: Admin document - `Social`: Social document - `AccountReport`: Accounting report - `Bank`: Bank document - `PermanentFolder`: Accountant folder - `Others`: Others - `<AnyOtherCustomCategoryName>`: Custom category name
  - FileName: string [example="myDocument.pdf"]  // 
  - Comment: string|null [example="here is my description."]  // 
  - KeyWords: array[string]  // 
  - ReferenceDateMonth: number [example=8]  // 
  - ReferenceDateYear: number [example=2022]  // 
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="akey7d06-c062-4681-a794-b7c22381dkr5"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## DELETE /library.documents.delete   [tags: Library Documents]
PAGE TEXT: Delete a library document, specified by its ID.
  param[query] Id *: string // 
RESPONSE 200: OK
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /invoices.sales.new   [tags: Invoices]
PAGE TEXT: Insert a sale invoice, which will then be converted into a book entry. The result will contain the generated book entry's id.
There are two ways to insert an invoice, either with or without an attached document.
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).
The accepted tax combinations (Tax rate / origin and type) are available [here](https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-sales.xlsx).
OP DESCRIPTION: Insert a sale invoice, which will then be converted into a book entry. The result will contain the generated book entry's id.

There are two ways to insert an invoice, either with or without an attached document.
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).

The accepted tax combinations (Tax rate / origin and type) are available [here](<https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-sales.xlsx>).
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Type *: number [example=0]  // 0 for an invoice, 1 for a credit note
  - Number *: number [example=201909001]  // The number of the invoice, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - DueDate *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
  - TotalAmount *: number [example=1210]  // 
  - BaseAmount *: number [example=1000]  // 
  - TaxAmount *: number [example=210]  // 
  - PaymentReferences: string|null [example="+++040/7139/58328+++"]  // 
  - PaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // *NULL* by default  - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - FileName: string|null [example="my-invoice.pdf"]  // Required if a document is attached. Include the file's extension.
  - Comment: string|null [example="my global comment"]  // 
  - MatchNo: number|null  // *NULL* By default.
  - Discount: object|null  // *NULL* By default. Information about a discount accorded if the payment is done within a given period of time.
      - Date: string(date-time)|null [example="2020-07-23T00:00:00+00:00"]  // The date until which the discount can be deduced from the total price. If none is provided, **7 days** will be added by default to the document's date.
      - Type: number enum[100, 150, 200] [example=100]  // Nullable. If none is provided, *ConditionalWithVat - 100* will be taken by default  - `100`: ConditionalWithVat : Cond. avec TVA - `150`: ConditionalWithoutVat : Cond. sans TVA - `200`: LimitedCredit : Pénalité de paiement
      - Rate: number [example=2.5]  // The rate of the discount to calculate based on the base amount provided. Provide a value between 0 and 100.
      - BaseAmount: number [example=1000]  // The base amount on which the discount is calculated.
      - Amount: number [example=25]  // The discount amount
  - CurrencyCode: string enum["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]  // *NULL* by default (= EUR). The folder must be configured to allow currencies for using this field.
  - CurrencyRate: number  // Nullable, rate of the day will be used by default
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - OverrideTaxAmounts: boolean [example=false]  // Nullable, false by default. By default, all tax amounts are recalculated (base amount X tax rate) and adapted if the provided tax amount is within 1 cent of the calculated one. If you want to force a specific tax amount, set this value to *true*.
  - AllowUnbalanced: boolean [example=false]  // Nullable, false by default. By default, all unbalanced book entries will be refuted. If you want to force it even though it's not balanced, set this value to *true*.
  - InvoiceLines *: array[object]  // 
      - Account *: string [example="700000"]  // The account's search key
      - BaseAmount *: number [example=1000]  // 
      - TaxAmount *: number [example=210]  // 
      - TaxRate *: number [example=21]  // 
      - TaxOrigin *: number enum[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] [example=0]  // - `0`: Vente nationale / Verkopen - `1`: Vente Cocontractant / Verkopen Medekontraktant - `2`: Exemption Art 44 / Vrijstellingen Art 44 - `3`: Vente Taxe d'égalisation / Verkopen EgalisatieBelasting - `4`: Vidanges-Emballages / Leeggoed-Verpakking - `5`: Escompte / Diskonto - `6`: Autre exemption / Andere Vrijstellingen - `7`: Autre exemption avec MAJ du C.A. / andere Vrijstell. met UPD v/d Omzet - `8`: Transfert de biens / Overdracht van Goederen - `9`: Ventes Marchandises / Verkopen Handelsgoederen - `10`: Livraison avec installation / Leveringen met installatie - `11`: Prestation hors Belgique / Diensten Buiten België - `12`: Travail à façon / Maakloonwerk - `13`: Vente taxe soumis dans le pays européen / Verkoopbelasting ingediend in het Europese land - `14`: Exportations / Exports - `15`: Ventes - `16`: Ventes Art 44 - `17`: Ventes de tabacs - `18`: Prestation de services - `19`: Prestations - `20`: Prestations hors Luxembourg
      - TaxType *: number enum[0, 1, 2] [example=0]  // - `0`: National - `1`: European - `2`: International
      - TaxCountryCode: string [example="FR"]  // Only used for OSS Vat lines (TaxOrigin = 13)
      - Comment: string [example="My comment for the line"]  // 
      - CostDistributionKey: string|null  // A cost distribution key as defined in Horus Office. When using a cost ditribution key, no cost lines must be specified. Cost lines will be used instead of cost distribution key if both are specified in the request.
      - CostLines: array[object]  // 
          - Amount *: number [example=1000]  // The sum of all cost lines' amounts must be equal to the corresponding invoice line's base amount.
          - Costs *: array[object]  // 
              - SchemaSearchKey *: string [example="DEPARTMENT"]  // The search key of an existing cost schema.
              - Value *: string [example="OFFICE"]  // The search key of an existing cost section, linked to this cost schema
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /invoices.sales.update   [tags: Invoices]
PAGE TEXT: Update a previously inserted sale invoice, which will then be converted into a book entry. The result will contain the **newly** generated book entry's id.
There are two ways to update an invoice, either with or without an attached document (the original attachment will be deleted in both cases).
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).
The accepted tax combinations (Tax rate / origin and type) are available [here](https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-sales.xlsx).
OP DESCRIPTION: Update a previously inserted sale invoice, which will then be converted into a book entry. The result will contain the **newly** generated book entry's id.

There are two ways to update an invoice, either with or without an attached document (the original attachment will be deleted in both cases).
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).

The accepted tax combinations (Tax rate / origin and type) are available [here](<https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-sales.xlsx>).
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Type *: number [example=0]  // 0 for an invoice, 1 for a credit note
  - Number *: number [example=201909001]  // The number of the invoice, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - DueDate *: string(date-time) [example="2019-09-04T00:00:00+00:00"]  // 
  - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
  - TotalAmount *: number [example=1210]  // 
  - BaseAmount *: number [example=1000]  // 
  - TaxAmount *: number [example=210]  // 
  - PaymentReferences: string|null [example="+++040/7139/58328+++"]  // 
  - PaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // *NULL* by default  - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - FileName: string|null [example="my-invoice.pdf"]  // Required if a document is attached. Include the file's extension.
  - Comment: string|null [example="my global comment"]  // 
  - MatchNo: number|null  // *NULL* By default.
  - Discount: object|null  // *NULL* By default. Information about a discount accorded if the payment is done within a given period of time.
      - Date: string(date-time)|null [example="2020-07-23T00:00:00+00:00"]  // The date until which the discount can be deduced from the total price. If none is provided, **7 days** will be added by default to the document's date.
      - Type: number enum[100, 150, 200] [example=100]  // Nullable. If none is provided, *ConditionalWithVat - 100* will be taken by default  - `100`: ConditionalWithVat : Cond. avec TVA - `150`: ConditionalWithoutVat : Cond. sans TVA - `200`: LimitedCredit : Pénalité de paiement
      - Rate: number [example=2.5]  // The rate of the discount to calculate based on the base amount provided. Provide a value between 0 and 100.
      - BaseAmount: number [example=1000]  // The base amount on which the discount is calculated.
      - Amount: number [example=25]  // The discount amount
  - CurrencyCode: string enum["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]  // *NULL* by default (= EUR). The folder must be configured to allow currencies for using this field.
  - CurrencyRate: number  // Nullable, rate of the day will be used by default
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - OverrideTaxAmounts: boolean [example=false]  // Nullable, false by default. By default, all tax amounts are recalculated (base amount X tax rate) and adapted if the provided tax amount is within 1 cent of the calculated one. If you want to force a specific tax amount, set this value to *true*.
  - AllowUnbalanced: boolean [example=false]  // Nullable, false by default. By default, all unbalanced book entries will be refuted. If you want to force it even though it's not balanced, set this value to *true*.
  - InvoiceLines *: array[object]  // 
      - Account *: string [example="700000"]  // The account's search key
      - BaseAmount *: number [example=1000]  // 
      - TaxAmount *: number [example=210]  // 
      - TaxRate *: number [example=21]  // 
      - TaxOrigin *: number enum[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] [example=0]  // - `0`: Vente nationale / Verkopen - `1`: Vente Cocontractant / Verkopen Medekontraktant - `2`: Exemption Art 44 / Vrijstellingen Art 44 - `3`: Vente Taxe d'égalisation / Verkopen EgalisatieBelasting - `4`: Vidanges-Emballages / Leeggoed-Verpakking - `5`: Escompte / Diskonto - `6`: Autre exemption / Andere Vrijstellingen - `7`: Autre exemption avec MAJ du C.A. / andere Vrijstell. met UPD v/d Omzet - `8`: Transfert de biens / Overdracht van Goederen - `9`: Ventes Marchandises / Verkopen Handelsgoederen - `10`: Livraison avec installation / Leveringen met installatie - `11`: Prestation hors Belgique / Diensten Buiten België - `12`: Travail à façon / Maakloonwerk - `13`: Vente taxe soumis dans le pays européen / Verkoopbelasting ingediend in het Europese land - `14`: Exportations / Exports - `15`: Ventes - `16`: Ventes Art 44 - `17`: Ventes de tabacs - `18`: Prestation de services - `19`: Prestations - `20`: Prestations hors Luxembourg
      - TaxType *: number enum[0, 1, 2] [example=0]  // - `0`: National - `1`: European - `2`: International
      - TaxCountryCode: string [example="FR"]  // Only used for OSS Vat lines (TaxOrigin = 13)
      - Comment: string [example="My comment for the line"]  // 
      - CostDistributionKey: string|null  // A cost distribution key as defined in Horus Office. When using a cost ditribution key, no cost lines must be specified. Cost lines will be used instead of cost distribution key if both are specified in the request.
      - CostLines: array[object]  // 
          - Amount *: number [example=1000]  // The sum of all cost lines' amounts must be equal to the corresponding invoice line's base amount.
          - Costs *: array[object]  // 
              - SchemaSearchKey *: string [example="DEPARTMENT"]  // The search key of an existing cost schema.
              - Value *: string [example="OFFICE"]  // The search key of an existing cost section, linked to this cost schema
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /invoices.sales.outstanding.list   [tags: Invoices]
PAGE TEXT: Get a list of open invoices (and/or linked payments) for a given folder, and eventually filter on company ids.
(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
OP DESCRIPTION: Get a list of open invoices (and/or linked payments) for a given folder, and eventually filter on company ids.

(**Sideloading** is supported for this request. More information about it can be found in the *Sideloading* section of the introduction.)
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - Filter: object  // All filters on *strings* are performed using the *contains* clause. It must match **all specified** filters in order to be included in the response.
      - CompanyIds: array[string]  // Filters on companies specified by their id.
      - ConfirmedOnly: boolean [example=false]  // *FALSE* by default. Include only entries confirmed by the accountant.
RESPONSE 200: OK -> object
  - Data: array[object]  // 
      - BookEntryNumber: string [example="2205002"]  // 
      - DaybookSearchKey: string [example="SALES"]  // 
      - Confirmed: boolean [example=true]  // 
      - CompanySearchKey: string [example="MY CLIENT"]  // 
      - TotalAmount: number [example=1210]  // 
      - TotalCurrencyAmount: number|null  // 
      - OpenAmount: number|null [example=1000]  // Specified only for open sale invoices and credit notes
      - OpenCurrencyAmount: number|null  // 
      - Currency: string|null  // 
      - TransactionType: number enum[0, 1, 2, 3] [example=0]  // - `0`: Sale invoice - `1`: Sale credit note - `2`: Payment - `3`: Miscellaneous operation
      - Date: string(date-time) [example="2022-05-01T00:00:00+00:00"]  // 
      - DueDate: string(date-time)|null [example="2022-05-31T00:00:00+00:00"]  // Specified only for open sale invoices and credit notes
      - LastPaymentDate: string|null  // Specified only for open sale invoices and credit notes
      - PaymentStatus: number|null enum[0, 10, 800] [example=10]  // Specified only for open sale invoices and credit notes  - `0`: Not paid - `10`: Partially paid - `800`: Paid
      - Remark: string|null [example="My invoice remark"]  // 
      - PaymentRemark: string|null [example="+++012/1234/12345+++"]  // 
      - LinkedElements: array[object]  // Specified only for open sale invoices and credit notes. Empty array for other transaction types.
          - BookEntryNumber: string [example="220065"]  // 
          - DaybookSearchKey: string [example="BANK"]  // 
          - Confirmed: boolean [example=true]  // 
          - TotalAmount: number [example=-210]  // 
          - TotalCurrencyAmount: number|null  // 
          - Currency: string|null  // 
          - TransactionType: number enum[0, 1, 2, 3] [example=2]  // - `0`: Sale invoice - `1`: Sale credit note - `2`: Payment - `3`: Miscellaneous operation
          - Date: string(date-time) [example="2022-05-10T00:00:00+00:00"]  // 
          - DueDate: string|null  // 
          - Remark: string [example="My bank transaction remark"]  // 
          - PaymentRemark: string|null  // 
          - Daybook: object  // 
              - Type: string [example="Daybooks"]  // 
              - Id: string [example="msjf8c7e-54d1-48d2-aed7-447e6003bc67"]  // 
          - BookEntry: object|null  // 
              - Type: string [example="BookEntries"]  // 
              - Id: string [example="zgfdg2be-8559-488a-b348-eeaqld4a735b"]  // 
          - AccountHistory: object  // 
              - Type: string [example="AccountHistories"]  // 
              - Id: string [example="eidhge75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Daybook: object  // 
          - Type: string [example="Daybooks"]  // 
          - Id: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
      - BookEntry: object|null  // 
          - Type: string [example="BookEntries"]  // 
          - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
      - AccountHistory: object  // 
          - Type: string [example="AccountHistories"]  // 
          - Id: string [example="djfh6e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Company: object|null  // 
          - Type: string [example="Companies"]  // 
          - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /invoices.sales.outstanding.info   [tags: Invoices]
PAGE TEXT: Get information about an open sale invoice/credit note, and its eventual linked elements (partial payments, etc.).
The folder id is always required, and **one of the following two** should also be included:
- The book entry id
- The book entry number (in the following format : {DaybookSearchKey}-{Number})
OP DESCRIPTION: Get information about an open sale invoice/credit note, and its eventual linked elements (partial payments, etc.).

The folder id is always required, and __one of the following two__ should also be included:
- The book entry id
- The book entry number (in the following format : {DaybookSearchKey}-{Number})
  param[query] Id: string // 
  param[query] BookEntryId: string // Specify either this or the book entry number.
  param[query] BookEntryNumber: string // Specify either this or the book entry id.
RESPONSE 200: OK -> object
  - Data: object  // 
      - BookEntryNumber: string [example="2205002"]  // 
      - DaybookSearchKey: string [example="SALES"]  // 
      - Confirmed: boolean [example=true]  // 
      - CompanySearchKey: string [example="MY CLIENT"]  // 
      - TotalAmount: number [example=1210]  // 
      - TotalCurrencyAmount: number|null  // 
      - OpenAmount: number|null [example=1000]  // Specified only for open sale invoices and credit notes
      - OpenCurrencyAmount: number|null  // 
      - Currency: string|null  // 
      - TransactionType: number enum[0, 1, 2, 3] [example=0]  // - `0`: Sale invoice - `1`: Sale credit note - `2`: Payment - `3`: Miscellaneous operation
      - Date: string(date-time) [example="2022-05-01T00:00:00+00:00"]  // 
      - DueDate: string(date-time)|null [example="2022-05-31T00:00:00+00:00"]  // Specified only for open sale invoices and credit notes
      - LastPaymentDate: string|null  // Specified only for open sale invoices and credit notes
      - PaymentStatus: number|null enum[0, 10, 800] [example=10]  // Specified only for open sale invoices and credit notes  - `0`: Not paid - `10`: Partially paid - `800`: Paid
      - Remark: string|null [example="My invoice remark"]  // 
      - PaymentRemark: string|null [example="+++012/1234/12345+++"]  // 
      - LinkedElements: array[object]  // Specified only for open sale invoices and credit notes. Empty array for other transaction types.
          - BookEntryNumber: string [example="220065"]  // 
          - DaybookSearchKey: string [example="BANK"]  // 
          - Confirmed: boolean [example=true]  // 
          - TotalAmount: number [example=-210]  // 
          - TotalCurrencyAmount: number|null  // 
          - Currency: string|null  // 
          - TransactionType: number enum[0, 1, 2, 3] [example=2]  // - `0`: Sale invoice - `1`: Sale credit note - `2`: Payment - `3`: Miscellaneous operation
          - Date: string(date-time) [example="2022-05-10T00:00:00+00:00"]  // 
          - DueDate: string|null  // 
          - Remark: string [example="My bank transaction remark"]  // 
          - PaymentRemark: string|null  // 
          - Daybook: object  // 
              - Type: string [example="Daybooks"]  // 
              - Id: string [example="msjf8c7e-54d1-48d2-aed7-447e6003bc67"]  // 
          - BookEntry: object|null  // 
              - Type: string [example="BookEntries"]  // 
              - Id: string [example="zgfdg2be-8559-488a-b348-eeaqld4a735b"]  // 
          - AccountHistory: object  // 
              - Type: string [example="AccountHistories"]  // 
              - Id: string [example="eidhge75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Daybook: object  // 
          - Type: string [example="Daybooks"]  // 
          - Id: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
      - BookEntry: object|null  // 
          - Type: string [example="BookEntries"]  // 
          - Id: string [example="0d6822be-8559-488a-b348-eeaqld4a735b"]  // 
      - AccountHistory: object  // 
          - Type: string [example="AccountHistories"]  // 
          - Id: string [example="djfh6e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Company: object|null  // 
          - Type: string [example="Companies"]  // 
          - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /invoices.purchases.new   [tags: Invoices]
PAGE TEXT: Insert a purchase invoice, which will then be converted into a book entry. The result will contain the generated book entry's id.
There are two ways to insert an invoice, either with or without an attached document.
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).
The accepted tax combinations (Tax type / kind / rate / origin / condition / condition value)) are available [here](https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-purchases.xlsx).
OP DESCRIPTION: Insert a purchase invoice, which will then be converted into a book entry. The result will contain the generated book entry's id.

There are two ways to insert an invoice, either with or without an attached document.
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).

The accepted tax combinations (Tax type / kind / rate / origin / condition / condition value)) are available [here](<https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-purchases.xlsx>).
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="dj568c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Type *: number [example=0]  // 0 for an invoice, 1 for a credit note
  - Number: number|null [example=202007001]  // Nullable. The number of the invoice, which will also be associated to the book entry (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2020-07-08T00:00:00+00:00"]  // 
  - DueDate *: string(date-time) [example="2020-07-08T00:00:00+00:00"]  // 
  - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
  - TotalAmount *: number [example=1210]  // 
  - BaseAmount *: number [example=1000]  // 
  - TaxAmount *: number [example=210]  // 
  - PaymentReferences: string|null [example="+++040/7139/58328+++"]  // 
  - PaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // *NULL* by default  - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - FileName: string|null [example="my-invoice.pdf"]  // Required if a document is attached. Include the file's extension.
  - Comment: string|null [example="my global comment"]  // 
  - MatchNo: number|null  // *NULL* By default.
  - VehicleId: string|null  // Nullable. If one is provided, the corresponding vehicle will be associated to every account history that uses an account requiring a vehicle.
  - Discount: object|null  // *NULL* By default. Information about a discount accorded if the payment is done within a given period of time.
      - Date: string(date-time)|null [example="2020-07-23T00:00:00+00:00"]  // The date until which the discount can be deduced from the total price. If none is provided, **7 days** will be added by default to the document's date.
      - Type: number enum[100, 150, 200] [example=100]  // Nullable. If none is provided, *ConditionalWithVat - 100* will be taken by default  - `100`: ConditionalWithVat : Cond. avec TVA - `150`: ConditionalWithoutVat : Cond. sans TVA - `200`: LimitedCredit : Pénalité de paiement
      - Rate: number [example=2.5]  // The rate of the discount to calculate based on the base amount provided. Provide a value between 0 and 100.
      - BaseAmount: number [example=1000]  // The base amount on which the discount is calculated.
      - Amount: number [example=25]  // The discount amount
  - CurrencyCode: string enum["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]  // *NULL* by default (= EUR). The folder must be configured to allow currencies for using this field.
  - CurrencyRate: number  // Nullable, rate of the day will be used by default
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - OverrideTaxAmounts: boolean [example=false]  // Nullable, false by default. By default, all tax amounts are recalculated (base amount X tax rate) and adapted if the provided tax amount is within 1 cent of the calculated one. If you want to force a specific tax amount, set this value to *true*.
  - AllowUnbalanced: boolean [example=false]  // Nullable, false by default. By default, all unbalanced book entries will be refuted. If you want to force it even though it's not balanced, set this value to *true*.
  - InvoiceLines *: array[object]  // 
      - Account *: string [example="612000"]  // The account's search key
      - BaseAmount *: number [example=1000]  // 
      - TaxAmount *: number [example=210]  // 
      - TaxRate *: number [example=21]  // 
      - TaxType *: number enum[0, 1, 2] [example=0]  // - `0`: National - `1`: European - `2`: International
      - TaxKind: number|null enum[0, 1, 2] [example=0]  // - `0`: MERCH (Merchandises) - `1`: GS (Goods and services) - `2`: INVEST (Investments)
      - TaxCondition: number|null enum[0, 1, 2, 3] [example=1]  // - `0`: COUNTRY (Country) - `1`: DEDUC (Deductible) - `2`: INVEST (Investments) - `3`: PCT (Percentage)
      - TaxConditionValue: string|null [example="true"]  // - `true`: DEDUC or INVEST - `false`: DEDUC or INVEST - `35`: PCT (35%) - `50`: PCT (50%) - `75`: PCT (75%) - `85`: PCT (85%)
      - TaxOrigin *: number enum[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39] [example=2]  // - `0`: Achat Biens et Services - `1`: Achat Investissements - `2`: Achat Marchandises - `3`: Achats de tabacs - `4`: Autres exemptions - `5`: Autres exemptions avec MAJ du C.A. - `6`: Biens Intracommunautaires - `7`: Biens taxés à l'origine - `8`: Cocontractant immobilier - `9`: Escompte - `10`: Frais de voiture / Multimédia - `11`: Frais généraux - `12`: Hors CEE sans facture - `13`: Import Biens et Services - `14`: Import Investissements - `15`: Import Marchandises - `16`: Intracommunautaire sans facture - `17`: Investissement biens Intracom. - `18`: Investissement partiellement récupérable - `19`: Investissement services intracom. - `20`: Investissements - `21`: Investissements taxés à l'origine - `22`: Livraisons de biens Art 46 - `23`: Livraisons de services Art 46 - `24`: Marchandises - `25`: Marchandises Intracommunautaires - `26`: Marchandises taxées à l'origine - `27`: Prestations - `28`: Prestations de sous-traitance - `29`: Report Biens et Services - `30`: Report Biens et Services Taxes dues par le preneur - `31`: Report Investissement - `32`: Report Investissement Taxes dues par le preneur - `33`: Report Marchandises - `34`: Report Marchandises Taxes dues par le preneur - `35`: Services Intracommunautaires - `36`: Services taxés à l'origine - `37`: Sous-traitance transport/consult. - `38`: Taxe déclarée en tant que débiteur Art 48 - `39`: Vidanges-Emballages
      - Comment: string [example="My comment for the line"]  // 
      - VehicleId: string|null  // Nullable. If one is provided, the corresponding vehicle will be associated to the account history, but only if the account requires it.
      - PersonalShare: object|null  // *NULL* By default. Information about a personal share to apply to this line.
          - PersonalSharePercentage: number [example=50]  // The percentage of the personal share to calculate based on the total amount of the line (= BaseAmount + TaxAmount) . Provide a value between 0 and 100.
          - PersonalShareAmount: number [example=605]  // The personal share amount (Total amount of invoice line * PersonalSharePercentage).
      - CostDistributionKey: string|null  // A cost distribution key as defined in Horus Office. When using a cost ditribution key, no cost lines must be specified. Cost lines will be used instead of cost distribution key if both are specified in the request.
      - CostLines: array[object]  // 
          - Amount *: number [example=1000]  // The sum of all cost lines' amounts must be equal to the corresponding invoice line's base amount.
          - Costs *: array[object]  // 
              - SchemaSearchKey *: string [example="DEPARTMENT"]  // The search key of an existing cost schema.
              - Value *: string [example="OFFICE"]  // The search key of an existing cost section, linked to this cost schema
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="ae8922be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /invoices.purchases.update   [tags: Invoices]
PAGE TEXT: Update a previously inserted purchase invoice, which will then be converted into a book entry. The result will contain the **newly** generated book entry's id.
There are two ways to update an invoice, either with or without an attached document (the original attachment will be deleted in both cases).
- When no document is attached, use the **application/json** content type as usual.
- For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.
The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).
The accepted tax combinations (Tax type / kind / rate / origin / condition / condition value)) are available [here](https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-purchases.xlsx).
OP DESCRIPTION: Update a previously inserted purchase invoice, which will then be converted into a book entry. The result will contain the **newly** generated book entry's id.

There are two ways to update an invoice, either with or without an attached document (the original attachment will be deleted in both cases).
* When no document is attached, use the **application/json** content type as usual.
* For joining a document to the invoice, use the **multipart/form-data** content type and add two arguments. The first one must be named **file** and contain the file's bytes, and the other one must be named **body** and contain the json-formatted information.

The total amount must be equal to the sum of the base amount and tax amount. Additionnally, the sum of each line's base amount must be equal to the global base amount (same for the tax amount).

The accepted tax combinations (Tax type / kind / rate / origin / condition / condition value)) are available [here](<https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-purchases.xlsx>).
REQUEST BODY (application/json) required: object
  - BookEntryId *: string [example="ae8922be-8559-488a-b348-eeaqld4a735b"]  // 
  - FolderId *: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
  - DaybookId *: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
  - Type *: number [example=0]  // 0 for an invoice, 1 for a credit note
  - Number: number|null [example=202007001]  // Nullable. The number of the invoice, which will also be associated to the book entry. (can be 0 if not confirmed)
  - Date *: string(date-time) [example="2020-07-08T00:00:00+00:00"]  // 
  - DueDate *: string(date-time) [example="2020-07-08T00:00:00+00:00"]  // 
  - CompanyId *: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
  - TotalAmount *: number [example=1210]  // 
  - BaseAmount *: number [example=1000]  // 
  - TaxAmount *: number [example=210]  // 
  - PaymentReferences: string|null [example="+++040/7139/58328+++"]  // 
  - PaymentMode: number enum[0, 100, 110, 200, 400, 410, 420, 900, 910]  // - `0`: Bank Transfer - `100`: Manual - `110`: Domiciliation - `200`: Credit Card - `400`: Paypal - `410`: Doccle - `420`: Digiteal - `900`: Check - `910`: Bill Draft
  - FileName: string|null [example="my-invoice.pdf"]  // Required if a document is attached. Include the file's extension.
  - Comment: string|null [example="my global comment"]  // 
  - MatchNo: number|null  // *NULL* By default.
  - VehicleId: string|null  // Nullable. If one is provided, the corresponding vehicle will be associated to every account history that uses an account requiring a vehicle.
  - Discount: object|null  // *NULL* By default. Information about a discount accorded if the payment is done within a given period of time.
      - Date: string(date-time)|null [example="2020-07-23T00:00:00+00:00"]  // The date until which the discount can be deduced from the total price. If none is provided, **7 days** will be added by default to the document's date.
      - Type: number enum[100, 150, 200] [example=100]  // Nullable. If none is provided, *ConditionalWithVat - 100* will be taken by default  - `100`: ConditionalWithVat : Cond. avec TVA - `150`: ConditionalWithoutVat : Cond. sans TVA - `200`: LimitedCredit : Pénalité de paiement
      - Rate: number [example=2.5]  // The rate of the discount to calculate based on the base amount provided. Provide a value between 0 and 100.
      - BaseAmount: number [example=1000]  // The base amount on which the discount is calculated.
      - Amount: number [example=25]  // The discount amount
  - CurrencyCode: string enum["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "HKD", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PLN", "RON", "RUB", "SEK", "SGD", "THB", "TRY", "USD", "ZAR"]  // *NULL* by default (= EUR). The folder must be configured to allow currencies for using this field.
  - Confirmed: boolean [example=false]  // Nullable, false by default
  - OverrideTaxAmounts: boolean [example=false]  // Nullable, false by default. By default, all tax amounts are recalculated (base amount X tax rate) and adapted if the provided tax amount is within 1 cent of the calculated one. If you want to force a specific tax amount, set this value to *true*.
  - AllowUnbalanced: boolean [example=false]  // Nullable, false by default. By default, all unbalanced book entries will be refuted. If you want to force it even though it's not balanced, set this value to *true*.
  - InvoiceLines *: array[object]  // 
      - Account *: string [example="612000"]  // The account's search key
      - BaseAmount *: number [example=1000]  // 
      - TaxAmount *: number [example=210]  // 
      - TaxRate *: number [example=21]  // 
      - TaxType *: number enum[0, 1, 2] [example=0]  // - `0`: National - `1`: European - `2`: International
      - TaxKind: number|null enum[0, 1, 2] [example=0]  // - `0`: MERCH (Merchandises) - `1`: GS (Goods and services) - `2`: INVEST (Investments)
      - TaxCondition: number|null enum[0, 1, 2, 3] [example=1]  // - `0`: COUNTRY (Country) - `1`: DEDUC (Deductible) - `2`: INVEST (Investments) - `3`: PCT (Percentage)
      - TaxConditionValue: string|null [example="true"]  // - `true`: DEDUC or INVEST - `false`: DEDUC or INVEST - `35`: PCT (35%) - `50`: PCT (50%) - `75`: PCT (75%) - `85`: PCT (85%)
      - TaxOrigin *: number enum[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39] [example=2]  // - `0`: Achat Biens et Services - `1`: Achat Investissements - `2`: Achat Marchandises - `3`: Achats de tabacs - `4`: Autres exemptions - `5`: Autres exemptions avec MAJ du C.A. - `6`: Biens Intracommunautaires - `7`: Biens taxés à l'origine - `8`: Cocontractant immobilier - `9`: Escompte - `10`: Frais de voiture / Multimédia - `11`: Frais généraux - `12`: Hors CEE sans facture - `13`: Import Biens et Services - `14`: Import Investissements - `15`: Import Marchandises - `16`: Intracommunautaire sans facture - `17`: Investissement biens Intracom. - `18`: Investissement partiellement récupérable - `19`: Investissement services intracom. - `20`: Investissements - `21`: Investissements taxés à l'origine - `22`: Livraisons de biens Art 46 - `23`: Livraisons de services Art 46 - `24`: Marchandises - `25`: Marchandises Intracommunautaires - `26`: Marchandises taxées à l'origine - `27`: Prestations - `28`: Prestations de sous-traitance - `29`: Report Biens et Services - `30`: Report Biens et Services Taxes dues par le preneur - `31`: Report Investissement - `32`: Report Investissement Taxes dues par le preneur - `33`: Report Marchandises - `34`: Report Marchandises Taxes dues par le preneur - `35`: Services Intracommunautaires - `36`: Services taxés à l'origine - `37`: Sous-traitance transport/consult. - `38`: Taxe déclarée en tant que débiteur Art 48 - `39`: Vidanges-Emballages
      - Comment: string [example="My comment for the line"]  // 
      - VehicleId: string|null  // Nullable. If one is provided, the corresponding vehicle will be associated to the account history, but only if the account requires it.
      - PersonalShare: object|null  // *NULL* By default. Information about a personal share to apply to this line.
          - PersonalSharePercentage: number [example=50]  // The percentage of the personal share to calculate based on the total amount of the line (= BaseAmount + TaxAmount) . Provide a value between 0 and 100.
          - PersonalShareAmount: number [example=605]  // The personal share amount (Total amount of invoice line * PersonalSharePercentage).
      - CostDistributionKey: string|null  // A cost distribution key as defined in Horus Office. When using a cost ditribution key, no cost lines must be specified. Cost lines will be used instead of cost distribution key if both are specified in the request.
      - CostLines: array[object]  // 
          - Amount *: number [example=1000]  // The sum of all cost lines' amounts must be equal to the corresponding invoice line's base amount.
          - Costs *: array[object]  // 
              - SchemaSearchKey *: string [example="DEPARTMENT"]  // The search key of an existing cost schema.
              - Value *: string [example="OFFICE"]  // The search key of an existing cost section, linked to this cost schema
REQUEST BODY (multipart/form-data) required: object
  - file *: string(binary)  // The file's bytes.
  - body *: string  // The JSON-formatted information (same structure as the `application/json` body).
RESPONSE 200: OK -> object
  - Id: string [example="0akd22be-8559-488a-b348-eeaqld4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /matching.next-number.customer   [tags: Matching]
PAGE TEXT: Get the next available "MatchNo" for a given customer.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - MatchNo: number [example=45]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /matching.next-number.supplier   [tags: Matching]
PAGE TEXT: Get the next available "MatchNo" for a given supplier.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - MatchNo: number [example=32]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /matching.next-number.account   [tags: Matching]
PAGE TEXT: Get the next available "MatchNo" for a given account.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - MatchNo: number [example=12]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## POST /matching   [tags: Matching]
PAGE TEXT: Do the matching between given account histories, based on a given (or auto-generated) "MatchNo".
All given account histories should be of the same *account type* (**100**: Customer, **200**: Supplier, **300**: General).
- With *account type* 100 or 200, all account histories should be linked to the same **company**.
- With *account type* 300, all account histories should be linked to the same **account**.
OP DESCRIPTION: Do the matching between given account histories, based on a given (or auto-generated) "MatchNo".

All given account histories should be of the same *account type* (**100**: Customer, **200**: Supplier, **300**: General).

- With *account type* 100 or 200, all account histories should be linked to the same **company**.

- With *account type* 300, all account histories should be linked to the same **account**.
REQUEST BODY (application/json) required: object
  - FolderId *: string [example="1a2752b0-310d-4ef4-bc9d-a82d8807c598"]  // 
  - MatchNo: number|null [example=15]  // *NULL* by default. If "AutoGenerateMatchNo* is set to *TRUE*, this value will be ignored.
  - AutoGenerateMatchNo: boolean [example=false]  // *FALSE* by default. If set to *TRUE*, the "MatchNo" value will be ignored and can be left to *NULL*.
  - AccountHistoryIds *: array[string] [example=["1a2752b0-310d-4ef4-bc9d-a82d8807c598", "1b2752b0-310d-4ef4-bc9d-a82d8807c598", "1c2752b0-310d-4ef4-bc9d-a82d8807c598"]]  // Array of strings, where each element is an account history's id.
RESPONSE 200: OK -> object
  - Data: object  // 
      - MatchNo: number [example=15]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object

==========================================================================================
## GET /book-entries.info   [tags: Book entries]
PAGE TEXT: Get details for a specific book entry.
  param[query] Id *: string // 
RESPONSE 200: OK -> object
  - Data: object  // 
      - Id: string [example="0d6822be-8559-488a-b348-eea0dd4a735b"]  // 
      - DocumentNo: number [example=1904001]  // 
      - Confirmed: boolean [example=true]  // 
      - Verified: boolean [example=true]  // False by default. Can only ever be set to 'True' if an additionnal verification step has been configured in Horus. Contact us for more info.
      - VerifiedBy: object|null  // Nullable. Only set if 'Verified' is set to 'True'.
          - Type: string [example="Users"]  // 
          - Id: string [example="45568715-39e3-449d-a87c-8ccfcf9be53a"]  // 
      - EntryType: number enum[0, 100, 400, 600, 800, 810, 850, 900, 910, 1000] [example=100]  // - `0`: Undefined - `100`: Normal - `400`: ManualMO - `600`: AutomaticMO - `800`: TemporaryClosingMO - `810`: AutomaticClosingMO - `850`: FiscalClosingMO - `900`: ResultReportMO - `910`: OpeningMO - `1000`: CostMO
      - OperationType: number enum[0, 100, 200, 300] [example=0]  // - `0`: Undefined - `100`: Vat - `200`: Reclassification - `300`: Depreciation
      - Date: string(date-time) [example="2019-04-04T00:00:00+00:00"]  // 
      - LastModifiedDate: string(date-time) [example="2019-04-06T00:00:00+00:00"]  // Date at which the record was last modified in the database.
      - CompanyDetail: object|null  // 
          - Company: object|null  // 
              - Type: string [example="Companies"]  // 
              - Id: string [example="32ebe925-23cc-4a3e-8b36-8b2b33780fc1"]  // 
          - RemarkPayment: string|null  // 
          - RemarkCompany: string|null  // 
          - DueDate: string|null  // 
          - PaymentDate: string|null  // 
          - TotalAmount: number|null  // 
          - TurnoverAmount: number|null  // 
          - TaxAmount: number|null  // 
          - DiscountDetail: object|null  // 
              - DiscountDate: string|null  // 
              - DiscountAmount: number|null  // 
              - DiscountRate: number|null  // 
      - Folder: object  // 
          - Type: string [example="Folders"]  // 
          - Id: string [example="83f26e75-f474-4b09-a1d3-aa698e18fbf0"]  // 
      - Daybook: object  // 
          - Type: string [example="Daybooks"]  // 
          - Id: string [example="87f48c7e-54d1-48d2-aed7-447e6003bc67"]  // 
      - Document: object|null  // 
          - Type: string [example="Documents"]  // 
          - Id: string [example="66cdb46b-0081-43f0-b398-ad81a4d79bc2"]  // 
      - AccountHistories: array[object]  // 
          - Type: string [example="AccountHistories"]  // 
          - Id: string [example="jdhrk2be-8559-488a-452r-eea0dd4a735b"]  // 
RESPONSE 400: Bad Request – the request contains invalid data or references non-existing resources. -> object
RESPONSE 401: Unauthorized – invalid, expired or missing access token.
RESPONSE 403: Forbidden – the user/integrator is not allowed to access this resource. -> object
RESPONSE 404: Not Found – the resource was not found. -> object
RESPONSE 500: Internal Server Error – something went wrong unexpectedly. -> object
```
