# Appendix: Horus Software API guides (extracted text)

Source: PDF prints of 15 guide pages from docs.horus-software.be (printed 13 Oct 2026), uploaded by Silas to Google Drive folder 'Horus guides'. Text extracted mechanically with pdftotext (left navigation column cropped); some navigation fragments and jumbled table cells remain. Not included: Quickstart, Register your integration, Support & FAQ, Changelog, the tax-combination spreadsheets and the Postman collection.

```text

==================================================================
## GUIDE: Authentication overview
==================================================================
user grants your integration access to the data available through their account,
without ever sharing their password with you.
Once the flow is complete, every API call is authenticated with a Bearer access
token:
Authorization: Bearer ACCESS_TOKEN

One API URL per license
Each fiduciary or SMB using Horus Office has its own database, hosted at its own
location. As a consequence, each license has its own API URL. This shapes the
                                Authentication overview

whole flow:
 Search 1. The authorization flow always starts
                                   ⌘K on the central Horus portal: Log In
 https://my-horus.com/fr/api (or https://my-horus.com/nl/api ).

2. During the flow, the user selects the license they want to connect.
 Guides
3. At the end ofAPItheReference
                      flow, your application receives the selected license's base
URL in the api_url parameter.
4. From then on, every request goes to that api_url : the token exchange,
e API               token refreshes and all API calls.
Your application ──(1) authorization request────────▶ my-
horus.com
                 ◀─(2) code + api_url ──────────────── (login +
license selection)

Your application ──(3) token exchange, API calls ───▶ api_url of
the selected license

🚧 Never hard-code the API URL
The api_url is different for every license. Read it from the
authorization redirect, store it with the connection, and use it as the base
URL for every request.
In this documentation, https://api.fiduciary.example stands for
"the api_url you received". It is not a real address.
               Connecting several licenses
            Authentication overview

rs             An integration can be connected to any number of licenses, for example when it
ces            serves many fiduciaries. Each connection is independent:
s operations        the user goes through the authorization flow once per license,
each connection has its own api_url , access token and refresh token,
always use a license's tokens with that license's api_url .
Store these values together, as one record per connected license.

What to read next
Authorization flow: every parameter of the authorization request, the redirect
and the token exchange.
Token lifecycle: access token expiry, refresh tokens and recommended
practices.
Prefer learning by doing? Follow the Quickstart.

   Quickstart                                               Authorization flow 

        Authentication overview


==================================================================
## GUIDE: Authorization flow
==================================================================
Authorization flow
                                                                                        Copy Page
                                                                                      Overview
Reference for the authorization request, the redirect and the token                                  Step 1 — Authorization request
exchange.                                                                                              The state parameter
                                                                                      Step 2 — User consent
                                                                                      Step 3 — Redirect to your
                                                                                      application
This page describes each step of the OAuth 2 authorization flow in detail. For a guided first run,     Access granted
see the Quickstart.                                                                                    Access denied
                                                                                      Step 4 — Token exchange
📘 Conventions                                                                                      Step 5 — Call the API
Values in capitals, such as YOUR_CLIENT_ID , are placeholders. URLs on the reserved              Security checklist
.example domain are fictitious: https://app.example/oauth/callback stands for
your redirect URL, and https://api.fiduciary.example for the api_url received
during the flow.

Overview
Step Who                        What happens
1    Your                       Redirects the user's browser to the Horus authorization page.
ns         application
2    The user                   Logs in, selects a license, and authorizes your integration.
3        Horus                  Redirects the browser to your redirect URL with a code , your
                   state and the license's api_url .

4        Your server            Exchanges the code for an access token and a refresh token, on
                  the api_url .
5        Your server            Calls the API on the api_url with the access token.
Step 1 — Authorization request
                        Authorization flow

Redirect the user's browser to:
GET https://my-horus.com/fr/api/oauth2/authorize

Use https://my-horus.com/nl/api/oauth2/authorize to display the Horus pages in
Dutch.
Parameter             Required    Description
client_id            Yes         Your integration's client ID.
response_type        Yes         Always code .
               The URL of the page in your application that
redirect_uri         Yes         receives the result. It must be registered for your
               integration.
               A random value generated by your application for
state                Recommended this request, returned unchanged in step 3. See The
                state parameter.

Query parameter values must be URL-encoded. Example:
https://my-horus.com/fr/api/oauth2/authorize?
client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=https%3A%2F%2Fapp.example%2Foauth%2Fcallback&state=Xk9pQ2vL7tRb

The state parameter
state protects your users against cross-site request forgery (CSRF). Without it, an attacker
could make a user's browser land on your callback with an authorization code of the attacker's
choosing, and connect the wrong license to your user's account.
1. Before redirecting, generate a random, unpredictable value (at least 16 random bytes).
2. Store it in the user's session.
3. Send it as state .
4. On the callback, compare the returned state with the stored value. If it is missing or
different, reject the request and do not exchange the code.
Use a new value for every authorization request. Never use a constant, a user ID or any other
guessable value.
Step 2 — User consent
                         Authorization flow

On the Horus pages, the user:
1. logs in with their Horus account,
2. selects the license to connect,
3. authorizes your integration to access the data available through their account.

Step 3 — Redirect to your application
Access granted
The user's browser is redirected to your redirect_uri with these parameters:
Parameter          Description
code              The authorization code, valid for 2 minutes.
state             The value sent in step 1. Verify it.
api_url           The base URL of the API of the license the user selected.
https://app.example/oauth/callback?
code=Hjhfn45k&state=Xk9pQ2vL7tRb4mZw&api_url=https://api.fiduciary.example

🚧 Store the api_url
api_url is specific to the selected license. Store it with the connection and use it for
the token exchange and every later request. Never hard-code it.

Access denied
If the user refuses, the browser is redirected to the same URL with an error parameter:
https://app.example/oauth/callback?error=access_denied

Step 4 — Token exchange
From your server, send a POST request to the token endpoint of the received api_url :

                                        Authorization flow

POST {api_url}/oauth2/access_token
Content-Type: application/x-www-form-urlencoded

Parameter                  Description
client_id                 Your integration's client ID.
client_secret             Your integration's client secret.
code                      The authorization code received in step 3.
grant_type                Must be auth_code .
redirect_uri              The same value as in step 1.

🚧 auth_code , not authorization_code
The Horus API expects grant_type=auth_code , which differs from the value used by
many OAuth 2 libraries. If you use such a library, check that you can override it.

Bash
curl -X POST "$API_URL/oauth2/access_token" \
-H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "client_id=YOUR_CLIENT_ID" \
--data-urlencode "client_secret=YOUR_CLIENT_SECRET" \
--data-urlencode "code=Hjhfn45k" \
--data-urlencode "grant_type=auth_code" \
--data-urlencode "redirect_uri=https://app.example/oauth/callback"

C#
// C#: exchange the authorization code on the license's api_url
var response = await http.PostAsync($"{apiUrl}/oauth2/access_token",
new FormUrlEncodedContent(new Dictionary<string, string>
{
["client_id"] = clientId,
["client_secret"] = clientSecret,
["code"] = code,
["grant_type"] = "auth_code",
["redirect_uri"] = "https://app.example/oauth/callback"
}));

Response:
                                             Authorization flow
JSON
{
"token_type": "Bearer",
"expires_in": 3600,
"access_token": "h4vtwzwlfip68zxLCJhbGhsgciO...",
"refresh_token": "8xLOxBtZp8r2tN3kq..."
}

Field                   Description
token_type           Always Bearer .
expires_in           Lifetime of the access token, in seconds (1 hour).
access_token         The token to send with every API request.
refresh_token        Single-use token to obtain a new token pair. See Token lifecycle.

Step 5 — Call the API
Send the access token in the Authorization header of every request, to the license's
api_url :

Bash
curl "$API_URL/users.me" \
-H "Authorization: Bearer $ACCESS_TOKEN"

Security checklist
The client_secret and the token exchange stay on your server.
state is random, stored per user session, and verified on every callback.

The authorization code is exchanged immediately (2-minute validity).
api_url , access token and refresh token are stored together, per license, and encrypted
at rest.
Tokens and secrets never appear in logs or URLs.

                                          Authorization flow
 Authentication overview                                        Token lifecycle 


==================================================================
## GUIDE: Token lifecycle
==================================================================
Token lifecycle
Access token expiry, refresh tokens and what to store for each
connection.

 📘 Conventions
    $API_URL stands for the api_url of the connected license, received
   during the authorization flow. Values in capitals, such as
    YOUR_CLIENT_ID , are placeholders.

Access tokens
Access tokens are Bearer tokens, sent in the Authorization header of every
request. They expire 1 hour after they are issued ( expires_in: 3600 , in
ATA             seconds).
               Refresh tokens
             Token lifecycle

rs             Every access token is issued together with a refresh token. When the access
ces            token expires, or shortly before, use the refresh token to obtain a new pair of
s operations   access token and refresh token, without involving the user.
POST {api_url}/oauth2/access_token
Content-Type: application/x-www-form-urlencoded

Parameter                          Description
client_id                         Your integration's client ID.
client_secret                     Your integration's client secret.
refresh_token                     The current refresh token.
grant_type                        Must be refresh_token .
Bash
curl -X POST "$API_URL/oauth2/access_token" \
-H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "client_id=YOUR_CLIENT_ID" \
--data-urlencode "client_secret=YOUR_CLIENT_SECRET" \
--data-urlencode "refresh_token=8xLOxBtZp8r2tN3kq..." \
--data-urlencode "grant_type=refresh_token"

The response has the same format as the initial token exchange and contains a
new access_token and a new refresh_token .
                  Token lifecycle

❗️ Refresh tokens are single-use
A refresh token can be used only once. Always save the new refresh
token returned with the new access token, replacing the previous one. If
you lose it, the user has to authorize your integration again.
Refresh tokens remain valid until the user revokes them or uninstalls your
integration. After that, the user has to go through the authorization flow again.

What to store for each connection
Store, on your server and for each connected license:
Value                   Why
      Base URL for every request and token refresh of this
api_url
      license.
access_token            Current Bearer token.
refresh_token           Needed to obtain the next token pair.
Expiry time             Computed from expires_in , to refresh before the
      token expires.
Treat tokens like passwords: encrypt them at rest and never write them to logs.

Recommended practices
                 Token lifecycle

Refresh proactively, a few minutes before the expiry time, rather than
waiting for a 401 response.
On a 401 Unauthorized response, refresh once and retry the request. If
the refresh fails, mark the connection as disconnected and ask the user to
authorize again.
Serialise refreshes per connection, with a lock or a queue. Two processes
refreshing at the same time with the same refresh token will make one of
them fail, since the token can only be used once.
Save the new token pair before using the new access token, so that a crash
cannot lose the only valid refresh token.
C#
// C#: refresh a connection's tokens (call under a per-connection
lock)
var response = await http.PostAsync($"
{connection.ApiUrl}/oauth2/access_token",
new FormUrlEncodedContent(new Dictionary<string, string>
{
["client_id"] = clientId,
["client_secret"] = clientSecret,
["refresh_token"] = connection.RefreshToken,
["grant_type"] = "refresh_token"
}));
response.EnsureSuccessStatusCode();

var tokens = await
response.Content.ReadFromJsonAsync<TokenResponse>();
connection.AccessToken = tokens.AccessToken;
connection.RefreshToken = tokens.RefreshToken;
connection.ExpiresAt =

                   Token lifecycle

DateTimeOffset.UtcNow.AddSeconds(tokens.ExpiresIn);
await repository.SaveAsync(connection);   // persist before using
the new token

record TokenResponse(
[property: JsonPropertyName("access_token")] string
AccessToken,
[property: JsonPropertyName("refresh_token")] string
RefreshToken,
[property: JsonPropertyName("expires_in")] int ExpiresIn);

   Authorization flow                                         Making requests 


==================================================================
## GUIDE: Making requests
==================================================================
Making requests
Endpoint naming, HTTP methods, content types and
compression.

 📘 Conventions
   In the examples, $API_URL stands for the api_url of the connected
   license and $ACCESS_TOKEN for a valid access token. See Quickstart.

Endpoints
The API consists of JSON-RPC-style methods exposed over HTTPS, in the form:
 {api_url}/{category}.{action}
                                Making requests

For example: users.me , companies.list , invoices.purchases.new , book-
entries.miscellaneous-operations.update .
ces             Action suffix                       Meaning
s operations     .list                              Retrieve a filtered list of entities.
.info                              Retrieve a single entity by its Id .
.new                               Create an entity.
.update                            Update an existing entity.
.delete    / .clear                Remove one / all related entities.
.download                          Download a file's bytes.
All identifiers ( Id , FolderId , CompanyId …) are GUIDs.

Headers
Header                   When            Value
                     Every                      followed by the access token
Authorization
                     request          Bearer

                     Requests         application/json       (recommended),
Content-Type
                     with a body      application/x-www-form-
                                     urlencoded    or multipart/form-data
                                      gzip , to receive compressed
Content-
Encoding
                     Optional        responses (see Gzip compression)
HTTP methods
Making requests

All methods must be called over HTTPS.
Kind of action                     HTTP          Arguments
                method
Simple reading ( .info ,                         Query string parameters, e.g.
.me )
                GET
                              companies.info?Id=…

Reading with complex                             Request body
filters (most .list )              POST

Creation and                                     Request body
modification                       POST

Deletion                           DELETE   or   See each endpoint in the API
                POST          Reference
A simple read with GET :
Bash
curl "$API_URL/companies.info?Id=32ebe925-23cc-4a3e-8b36-
8b2b33780fc1" \
-H "Authorization: Bearer $ACCESS_TOKEN"

📘 Why POST for reading?
Reading actions with complex arguments (filters, arrays, date ranges)
use POST , so that arguments are easy to build and never exceed the
                 Making requests

maximum URL length.

Request bodies
Bodies can be sent as JSON or URL-encoded data. Set the Content-Type
header accordingly:
Format                       Header
JSON
(recommended)                 Content-Type: application/json

URL-encoded                   Content-Type: application/x-www-form-
          urlencoded

File upload                   Content-Type: multipart/form-data   (see
          Documents & attachments)
We strongly recommend JSON: it makes complex arguments such as nested
objects and arrays much easier to build.
Bash
curl -X POST "$API_URL/companies.list" \
-H "Authorization: Bearer $ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"Filter": { "IsCustomer": true, "Name": "Horus" }
}'

Filters
Making requests

Most .list endpoints accept a Filter object:
filters on strings use a contains comparison (e.g. "Name": "Horus"
matches Horus Software), unless stated otherwise in the API Reference;
an entity must match all specified filters to be returned;
omitted or null filters are ignored.
Many lists also offer ModifiedAfter / ModifiedBefore filters, which are ideal
for incremental synchronisation (see Reading accounting data).

Dates
Dates are exchanged as ISO 8601 strings with a time zone offset, e.g. 2019-09-
04T00:00:00+00:00 .

Partial updates
On .update endpoints for master data (companies, accounts, daybooks…),
provide only the fields you want to change, or leave them null :
null or omitted → the current value is kept;

"" (empty, non-null string) → the current value is erased.

Gzip compression
                   Making requests

Gzip compression is available on every endpoint and highly recommended to
reduce payload sizes. Add a Content-Encoding: gzip header to your request
and the response will be gzipped automatically.

   Token lifecycle                                        Responses & errors 


==================================================================
## GUIDE: Responses & errors
==================================================================
Responses & errors
Response envelope, status codes and error format.

Successful responses
Reading data
Responses containing information are JSON objects with the payload under a top-
level Data key. Data is an object for single entities and an array for lists.
 JSON
 {
                                                                       
     "Data": {
       "Id": "14feb291-8b47-44c6-8cbb-97a3f24c33c8",
       "FirstName": "Robert",
       "LastName": "Doe",
       "Email": "robert@fiduciary.example",
ATA                        "CreationDate": "2018-03-16T15:16:35+00:00",

                                 Responses & errors

     "PhoneNumber": "0497/12 34 56",
     "Language": "FR",
rs                       "IsAccountant": true

ces              }
 }

When sideloading is used, related entities are returned next to Data under an
Included key.

Creating or updating data
Requests that create or update an entity return only its identifier:
JSON
{
 "Id": "14feb291-8b47-44c6-8cbb-97a3f24c33c8"
}

🚧 Updating book entries returns a new Id
Updating an invoice or an operation ( invoices.*.update , book-
entries.*.update ) generates a new book entry. The response
contains the new book entry's Id: replace the Id stored on your side.

Relationships
Related entities are represented by a type/id reference:
                      Responses & errors

JSON
"ResponsibleUser": {
"Type": "Users",
"Id": "14feb291-8b47-44c6-8cbb-97a3f24c33c8"
}

Use the matching .info endpoint, or sideloading where available, to retrieve the
related entity.

Status codes
Code Meaning
200 OK.
Bad Request: the request contains invalid data or references non-
400
existing resources.
401 Unauthorized: the access token is invalid, expired or missing.
Forbidden: the user or integration is not allowed to access this
403
resource.
404 Not Found: the resource was not found.
500 Internal Server Error: something went wrong unexpectedly.

Error format
                        Responses & errors

Except for authorization errors, errors return an object with three fields:
JSON
{
"ErrorType": "not_found",
"Details": "The requested book entry was not found.",
"Message": "Element was not found"
}

Field                Description
ErrorType          Machine-readable error category. Use it in your code.
Details            Human-readable explanation of what went wrong.
Message            Short, generic message.

Handling errors
401  : refresh the access token once and retry (see Token lifecycle). If it fails
again, ask the user to reconnect.
400 : do not retry as-is. Log Details , it usually points to the invalid field or
the missing reference (unknown account, unbalanced entry, etc.).
500 : retry later with exponential backoff. If the error persists, contact
developer@horus-software.be with the endpoint, the timestamp and the
request body.
                     Responses & errors

   Making requests                                         Sideloading 


==================================================================
## GUIDE: Sideloading
==================================================================
Sideloading
Retrieve related entities in a single request.

Sideloading lets you retrieve related items as part of a single request, instead of
calling .info for each relationship.

How it works
Relationships are always represented by a type/id object. For example, a book
entry references a company:
 JSON
 {
     "Data": {
       "Id": "0d6822be-8559-488a-b348-eea0dd4a735b",
ATA                        "DocumentNo": 1904001,
       "CompanyDetail": {
                                   Sideloading

        "Company": {
          "Type": "Companies",
rs                            "Id": "32ebe925-23cc-4a3e-8b36-8b2b33780fc1"

ces                         },
        "RemarkPayment": null,
s operations                "RemarkCompany": null
    }
}
}

To sideload a relationship, add an Include parameter to the JSON body,
containing the dot-notation path of the relationship property:
JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"DaybookId": "87f48c7e-54d1-48d2-aed7-447e6003bc67",
"StartMonth": 1, "StartYear": 2019,
"EndMonth": 12, "EndYear": 2019,
"Include": "CompanyDetail.Company"
}

The related entities are returned in an Included property, indexed by object
type:
JSON
{
"Data": [ ... ],
"Included": {
  "Companies": [
                       Sideloading

{
"Id": "32ebe925-23cc-4a3e-8b36-8b2b33780fc1",
"SearchKey": "HORUS",
"Name": "Horus Software",
"Address": "Quai des ardennes, 9"
}
]
}
}

To resolve a relationship, use its Type to find the right collection in Included ,
then its Id to find the entity.

Multiple relationships
Pass several paths as a comma-separated value:
JSON
"Include": "CompanyDetail.Company,Daybook,Folder"

Supported endpoints
Sideloading is currently supported on:
book-entries.list

account-histories.list

companies.list

                    Sideloading

invoices.sales.outstanding.list

If you need it on another endpoint, contact us at developer@horus-software.be.

   Responses & errors                                           Data model 


==================================================================
## GUIDE: Data model
==================================================================
Data model
The main Horus Office entities and how they relate to each other.

Understanding a few Horus Office concepts will make the API Reference much
easier to navigate. If you are familiar with Belgian accounting, most of them will
sound natural.
 License (fiduciary / SMB)
                                                                             
  └── Users
  └── Folders ─────────────── one per company whose accounts are
 kept
       ├── Fiscal years
       ├── Daybooks           (purchases, sales, bank, misc.
 operations…)
       ├── Accounts           (the folder's chart of accounts)
       ├── Companies          (customers, suppliers,
 beneficiaries) ── IBANs
ATA                        ├── Vehicles

                                 Data model

    ├── Cost schemas ── Cost sections          (analytics)
    ├── Book entries ── Account history lines ── Cost histories
rs                      │        └── Documents (main document + annexes)

ces                     └── Library documents

Licenses and users
A license represents a Horus Office customer: a fiduciary (accounting firm) or an
SMB. Each license has its own database and its own API endpoint (see
Authentication overview).
 licenses.main returns the main license, i.e. the fiduciary/SMB license.

 licenses.me returns the license linked to the authenticated user.

Users are either accountants using Horus Office ( IsAccountant: true ) or
entrepreneurs using Horus Mobile. What a user can see through the API depends
on their access in Horus.

Folders
A folder is the accounting record of one company: its configuration, chart of
accounts, daybooks and entries. Almost every endpoint requires a FolderId .
folders.list takes a Mode :

Mode               Accountant                     Entrepreneur
0 — All                                          All folders they have
folders            All folders.                   access to.
                   Data model

Mode                Accountant                   Entrepreneur
1 — My             Folders they are responsible All folders they have
folders             for.                         access to.
Folders also tell you which optional modules are enabled, such as WithAssets
and WithAnalytics .

Fiscal years
A fiscal year (accounting exercise) belongs to a folder and describes its closing
status: start and end dates, last VAT closure date, last closure dates per type of
daybook (purchases, sales, financials, miscellaneous operations), and whether
the year IsClosed .
📘 Check closure dates before posting
Before pushing entries, check the relevant closure dates with fiscal-
years.list to avoid posting into a period that has already been closed
by the accountant.

Daybooks
A daybook is an accounting journal. Every book entry is stored in one, depending
on its type. The daybook Type drives which endpoint you use to post entries:

                  Data model

Daybook type                  Value     Endpoint to post entries
Purchase / Purchase            100 /
credit note                   150
                      invoices.purchases.new

Sale / Sale credit note       200   /    invoices.sales.new
           250

Bank                          500        book-entries.banks.new

Financial                     590        book-entries.financials.new

Miscellaneous                            book-entries.miscellaneous-
operation                     600
                     operations.new

Other types exist (cash, temporary or system miscellaneous operations, budget,
external). See the daybooks.info reference for the full list. Daybooks are
identified by a SearchKey (e.g. ACH , VEN ).

Accounts
Every folder has its own chart of accounts. Each account is identified by a unique
search key, which is usually the account number (e.g. 400000 , 604000 ,
700000 ). When posting entries, you reference accounts by their search key.

Accounts carry their category, VAT settings, matchability ( IsMatchable ),
personal share settings, and more.

Companies
                   Data model

Companies are the legal entities a folder deals with: customers, suppliers and
beneficiaries (e.g. employees receiving salaries). They are usually identified by a
VAT number and/or a local business number, and by a SearchKey .
A company has:
its customer and supplier concentration accounts (e.g. 400000 and
440000 ),

payment terms and usual payment modes,
one or more IBANs, managed with the ibans.* endpoints.

Book entries and account histories
A book entry (accounting entry) is an accounting transaction in a folder, in a
daybook, at a given date. It may be linked to a dematerialised document (PDF,
image…).
The entry's detailed lines are its account history lines: one line per account
movement, with debit/credit amounts, VAT information, matching number, etc.
book-entries.list returns entries for a daybook and a period.

account-histories.list returns every entry line of a folder over a period.
This is the general ledger view.
account-balance.list returns the debit/credit state of each account over
a period.
Confirmed and unconfirmed entries
                  Data model

Entries can be confirmed or not. Entries pushed through the API are unconfirmed
by default ( Confirmed: false ), which lets the accountant review them in Horus
Office before confirming them. Some operations, such as deleting a
miscellaneous operation, are only possible on unconfirmed entries.

Analytics: cost schemas, sections and histories
When the analytics module is enabled ( WithAnalytics ), entry lines can be
distributed across analytical dimensions:
a cost schema is an analytical dimension (e.g. DEPARTMENT ). A folder can
use up to 8 cost schemas;
a cost section is a value within a schema (e.g. OFFICE );
cost histories are the analytical distribution of account history lines;
a cost distribution key is a predefined distribution, configured in Horus
Office, that you can reference instead of detailing cost lines.

Vehicles
Vehicles are tracked for accounts that require them (car expenses, for example).
When posting purchases or operations, you can pass a VehicleId so that it is
associated with the relevant lines.

Documents and library documents
A document is a dematerialised file linked to a book entry, as its main
document or as an annex.
                    Data model

A library document is a file stored in the folder's library, not linked to any
book entry.
See Documents & attachments.

Search keys and Ids
Entities are identified by a GUID Id , used in API references ( FolderId ,
CompanyId , DaybookId …). Many of them also have a human-readable search
key ( SearchKey ), unique within the folder. Accounts and cost schemas/sections
are referenced by search key in posting endpoints.

   Sideloading                                         Reading accounting data 


==================================================================
## GUIDE: Reading accounting data
==================================================================
Reading accounting data
Navigate folders, ledgers and balances, and keep your data in
sync.

  📘 Conventions
    In the examples, $API_URL stands for the api_url of the connected
    license and $ACCESS_TOKEN for a valid access token. See Quickstart.

This guide shows the typical sequence of calls used to read data from a Horus
Office folder.

1. Find the folder
ATA                   Bash
                              Reading accounting data

curl -X POST "$API_URL/folders.list" \
rs                 -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type:
application/json" \
ces                -d '{ "Mode": 0, "Filter": { "VatNumber": "BE0000000097",
s operations     "IsVatLiable": true } }'

Keep the folder Id : it is the FolderId used by nearly every other endpoint.

2. Load the reference data
Reference data changes rarely. Load it once and cache it per folder:
Data                                    Endpoint
Fiscal years and closure dates          fiscal-years.list

Daybooks (journals)                     daybooks.list

Chart of accounts                       accounts.list

Customers, suppliers,
beneficiaries                           companies.list

Vehicles                                vehicles.list

Analytics (if WithAnalytics )           cost-schemas.list   , cost-
                                    sections.list

3. Read entries and ledgers
                        Reading accounting data

Periods are expressed by month and year ( StartMonth , StartYear ,
EndMonth , EndYear ).

Book entries of a daybook
book-entries.list          returns the entries of one daybook over a period:
JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"DaybookId": "87f48c7e-54d1-48d2-aed7-447e6003bc67",
"StartMonth": 1, "StartYear": 2024,
"EndMonth": 12, "EndYear": 2024,
"Filter": { "ConfirmedOnly": true }
}

Use book-entries.info to get the full detail of one entry.
Account histories (general ledger)
account-histories.list       returns every entry line of the folder over a period,
across all daybooks. Useful filters include:
Filter                                              Usage
                                          Restrict to accounts starting
                                          with the given keys, e.g.
                                           ["6", "7"] for P&L
AccountSearchKeys

                                          accounts.
                        Reading accounting data

Filter                                             Usage
     / ExcludedDaybookIds                Include or exclude specific
DaybookIds
                                         daybooks.
                                         Lines of one customer or
CompanyId
                                         supplier.
                                         Only lines that are not
NotMatchedOnly
                                         matched yet.
                                         Only entries confirmed by the
ConfirmedOnly
                                         accountant.
IncludeCompanyDetail             ,
IncludeMatchDetail           ,                    Enrich each line with
IncludeVatDetail         ,                        additional details.
IncludeCostDetail

Account balance (trial balance)
account-balance.list   returns the debit/credit state of each account over a
period. Use AccountSearchKeys to narrow it down and
IncludeUnusedAccounts to include accounts without movement.

Outstanding items
Need                                    Endpoint
Open items of customers                 customers.outstanding

                        Reading accounting data

Need                                   Endpoint
Open items of suppliers                suppliers.outstanding

Open sales invoices and their          invoices.sales.outstanding.list       /
linked payments                        .info

See Outstanding items & matching.

Confirmed vs. unconfirmed data
By default, lists include unconfirmed entries, i.e. entries not yet validated by the
accountant. For reporting based on validated figures, set ConfirmedOnly:
true .

Incremental synchronisation
To keep a local copy in sync without reloading everything, use the
ModifiedAfter filter, available on companies.list , book-entries.list and
account-histories.list among others:

1. Run a full load once and record the time at which you started it.
2. On the next run, pass that time as ModifiedAfter and only process what
changed.
3. Store the new start time for the following run.
JSON

                         Reading accounting data

{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"StartMonth": 1, "StartYear": 2024,
"EndMonth": 12, "EndYear": 2024,
"Filter": { "ModifiedAfter": "2024-06-01T00:00:00+00:00" }
}

🚧 Updated entries get a new Id
When an invoice or an operation is updated, a new book entry is
generated. When synchronising entries, do not rely on the Id alone to
detect changes; also reconcile on business identifiers such as the
daybook and the entry number.

Reduce round trips
Use sideloading with Include to fetch related companies, daybooks or
folders together with entries.
Enable gzip compression for large ledgers.

    Data model                                     Managing customers & 
                                                     suppliers

         Reading accounting data


==================================================================
## GUIDE: Managing customers & suppliers
==================================================================
Managing customers & suppliers
Create, update and look up companies and their bank accounts.

Companies are the customers, suppliers and beneficiaries of a folder. Invoices
and customer/supplier entry lines reference them through CompanyId , so you
usually need to find or create the company first.

Find an existing company
Search by VAT number, name, search key or external reference with
companies.list :

 JSON
 {
                                                                         
     "FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
                          Managing customers & suppliers

"Filter": { "VatNumber": "BE0478696879" }
}
s operations    📘 Use ExternalReference for your own identifiers
Store your system's identifier in the company's ExternalReference
field when you create it. You can then filter on it to find the company
again reliably.

Create a company
companies.new  requires FolderId , SearchKey , Name , IsCustomer ,
IsSupplier , IsVatLiable , LanguageCode and CountryCode :

JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"SearchKey": "HORUS",
"Name": "Horus Software",
"IsCustomer": true,
"IsSupplier": false,
"IsVatLiable": true,
"VatNumber": "BE0478696879",
"LanguageCode": "FR",
"CountryCode": "BE",
"Address": "Quai des Ardennes 9",
"ZipCode": "4020",
"Locality": "Liège",
"CustomerPaymentDelay": "30E",
                 Managing customers & suppliers

"ExternalReference": "CRM-000123",
"Ibans": [
{ "Iban": "BE72000000001616", "Bic": "BPOTBEB1", "IsDefault":
true, "IsDomiciliation": false }
]
}

The response contains the new company's Id .
Notes:
By default, a VAT number already used by another company is refused. Set
AllowDuplicateVatNumber: true to allow it deliberately.

CustomerConcentrationAccount and SupplierConcentrationAccount
are optional and let you set the concentration accounts explicitly (e.g.
400000 , 440000 ).

Payment terms format
CustomerPaymentDelay             and SupplierPaymentDelay follow the format
999[D|J|M][E|F|e|f]          :
Example                Meaning
30E                   30 days, end of month
15e                   15th of the next month
2M                    In 2 months, same day as the invoice

                 Managing customers & suppliers

D  / J stand for days and M for months; E / F mean end of month, e / f start
of next month.

Update a company
companies.update        follows the partial update rule: send only the fields to
change.
JSON
{
"CompanyId": "32ebe925-23cc-4a3e-8b36-8b2b33780fc1",
"InvoiceEmail": "billing@horus-software.be",
"PhoneNumber": ""
}

Here InvoiceEmail is changed, PhoneNumber is erased (empty string), and
every other field is left untouched.

Bank accounts (IBANs)
Action                                              Endpoint
List a company's IBANs                               ibans.list

Add an IBAN                                          ibans.new

Remove one IBAN                                      ibans.delete

Remove all IBANs                                     ibans.clear

                   Managing customers & suppliers

   Reading accounting data                            Posting sales & purchase 
                                                          invoices


==================================================================
## GUIDE: Posting sales & purchase invoices
==================================================================
Posting sales & purchase invoices
Push invoices and credit notes, with or without their PDF, as book
entries.

 📘 Conventions
   In the examples, $API_URL stands for the api_url of the connected
   license and $ACCESS_TOKEN for a valid access token. See Quickstart.

Sales and purchase invoices pushed through the API are converted into book
entries in the corresponding daybook. The response contains the generated book
entry's Id .
 Action     Sales                                  Purchases
ATA                  Create      invoices.sales.new                    invoices.purchases.new

                          Posting sales & purchase invoices

Action      Sales                             Purchases
rs              Update       invoices.sales.update            invoices.purchases.update
Before you start
You need:
1. the FolderId ,
2. the DaybookId of a sales or purchase daybook ( daybooks.list , types
 200 / 250 for sales and 100 / 150 for purchases),

3. the CompanyId of the customer or supplier, found or created as described in
Managing customers & suppliers,
4. the search keys of the accounts to book each line on ( accounts.list ),
e.g. 700000 for sales or 612000 for purchases.

Create a sales invoice
JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"DaybookId": "87f48c7e-54d1-48d2-aed7-447e6003bc67",
"Type": 0,
"Number": 202409001,
"Date": "2024-09-04T00:00:00+00:00",
"DueDate": "2024-10-04T00:00:00+00:00",
"CompanyId": "32ebe925-23cc-4a3e-8b36-8b2b33780fc1",

             Posting sales & purchase invoices

"TotalAmount": 1210,
"BaseAmount": 1000,
"TaxAmount": 210,
"PaymentReferences": "+++040/7139/58328+++",
"Comment": "Invoice 2024-09-001",
"InvoiceLines": [
{
"Account": "700000",
"BaseAmount": 1000,
"TaxAmount": 210,
"TaxRate": 21,
"TaxOrigin": 0,
"TaxType": 0,
"Comment": "Consulting services"
}
]
}

JSON
{ "Id": "0d6822be-8559-488a-b348-eea0dd4a735b" }

Type    is 0 for an invoice and 1 for a credit note.

Amount rules
The API checks that the invoice is consistent:
TotalAmount = BaseAmount + TaxAmount ;

the sum of the lines' BaseAmount = the invoice's BaseAmount ;
            Posting sales & purchase invoices

the sum of the lines' TaxAmount = the invoice's TaxAmount .
Two options let you relax these checks when needed:
Option                                Default Effect
                           Tax amounts are recalculated (base ×
                           rate) and adapted when the provided
OverrideTaxAmounts                   false
                           amount is within 1 cent. Set to true to
                           force your own tax amounts.
                           Unbalanced book entries are refused.
AllowUnbalanced                      false   Set to true to force the entry even
                           though it is not balanced.

VAT on invoice lines
Each line carries its VAT treatment through a combination of fields:
Field                                                             Sales Purchases
TaxRate                                                          ✔        ✔

TaxType   ( 0 National, 1 European, 2
International)                                                    ✔        ✔

TaxOrigin                                                        ✔        ✔

TaxKind  ( 0 Merchandises, 1 Goods & services,
2 Investments)
                                                        ✔

            Posting sales & purchase invoices

Field                                                       Sales Purchases
TaxCondition / TaxConditionValue                                     ✔

TaxCountryCode (OSS lines only, TaxOrigin = 13)            ✔

Only some combinations are valid. The accepted combinations are listed in these
reference files:
Accepted tax combinations for sales
Accepted tax combinations for purchases

Purchase-specific options
Purchase invoices support a few additional fields:
VehicleId , at invoice or line level: associates a vehicle with lines whose
account requires one;
PersonalShare on a line: the private portion of the expense, as a
percentage of the line's total (base + tax) and the corresponding amount.
JSON
"InvoiceLines": [
{
"Account": "612000",
"BaseAmount": 1000,
"TaxAmount": 210,
"TaxRate": 21,
"TaxType": 0,

             Posting sales & purchase invoices

"TaxKind": 0,
"TaxCondition": 1,
"TaxConditionValue": "true",
"TaxOrigin": 2,
"PersonalShare": { "PersonalSharePercentage": 50,
"PersonalShareAmount": 605.0 }
}
]

Optional features
Feature     Fields                                  Notes
Payment      PaymentReferences ,                    E.g. a structured communication
information PaymentMode                              +++040/7139/58328+++ .

Cash                                                Rate, amount and deadline. If no
discount              Discount                      date is given, 7 days are added
                                 to the invoice date.
                                  null means EUR. The folder
Foreign               CurrencyCode              ,   must be configured to allow
currency              CurrencyRate                  currencies. If no rate is given,
                                 the rate of the day is used.
                                 Pre-assign a matching number
Matching              MatchNo                       (see Outstanding items &
                                 matching).
Analytics             CostLines           or        The sum of a line's cost lines
   CostDistributionKey           must equal its BaseAmount . If
            Posting sales & purchase invoices

Feature             Fields                     Notes
 per line                   both are provided, cost lines
                            take precedence.

Confirmation and numbering
Confirmed    is false by default: the invoice is created as an unconfirmed entry
that the accountant can review in Horus Office. Number is the invoice number
associated with the book entry. It can be 0 when the invoice is not confirmed.

Attaching the invoice document
To send the invoice's PDF (or image/XML) together with the data, use
multipart/form-data with two fields, file and body , and set FileName :

Bash
curl -X POST "$API_URL/invoices.purchases.new" \
-H "Authorization: Bearer $ACCESS_TOKEN" \
-F "file=@supplier-invoice-2024-118.pdf" \
-F 'body={
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"DaybookId": "9d0c7b6a-5e4f-4a3b-8c2d-1e0f9a8b7c6d",
"Type": 0,
"Number": 0,
"Date": "2024-09-04T00:00:00+00:00",
"DueDate": "2024-10-04T00:00:00+00:00",
"CompanyId": "32ebe925-23cc-4a3e-8b36-8b2b33780fc1",
"TotalAmount": 121,
"BaseAmount": 100,
           Posting sales & purchase invoices

"TaxAmount": 21,
"FileName": "supplier-invoice-2024-118.pdf",
"InvoiceLines": [
{ "Account": "612000", "BaseAmount": 100, "TaxAmount":
21, "TaxRate": 21,
"TaxType": 0, "TaxKind": 0, "TaxCondition": 1,
"TaxConditionValue": "true", "TaxOrigin": 2 }
]
}'

See Documents & attachments for details.

Updating an invoice
invoices.sales.update       and invoices.purchases.update take the
BookEntryId of the invoice plus the complete invoice payload (same required
fields as creation):
the response contains the newly generated book entry's Id : replace the
one stored on your side;
the original attachment is deleted in both cases. Send the document again
with multipart/form-data if it should be kept.

🚧 Updates are full replacements
Unlike master data updates (companies, accounts…), invoice updates are
not partial: send the full invoice as it should be after the update.

             Posting sales & purchase invoices

Managing customers &                                          Bank, financial &
   suppliers                                            miscellaneous operations 


==================================================================
## GUIDE: Bank, financial & miscellaneous operations
==================================================================
Bank, financial &
                                                           Copy Page

miscellaneous
                                                         Line types
                                                         Bank operations

operations                                                              Financial operations
                                                         Miscellaneous operations (
                                                           Updating and deleting
Post bank statements, financial operations and                          Numbering
miscellaneous operations (OD).

Besides invoices, the API lets you post three kinds of
operations as book entries:
Operation           Daybook Create                         Update
         type
Bank                Bank      book-                        book-
operation           ( 500 ) entries.banks.new              entries.banks.update

Financial           Financial book-                        book-
operation           ( 590 ) entries.financials.new         entries.financials.update

                          Bank, financial & miscellaneous operations

Operation           Daybook Create                                Update
erations                        type
Miscellaneous Misc.                      book-
                                                          book-

operation     operation                 entries.miscellaneous-
                                                          entries.miscellaneous-
                                                                              ,
(OD)          ( 600 )                   operations.new
                                                          operations.update
                                                          .lines.update

All three return the generated book entry's Id , can carry an
attached document ( multipart/form-data , see
Documents & attachments) and are unconfirmed by default.

Line types
Lines reference an account by search key and a line type:
Type         Meaning                                 CompanyId

1            Customer                               Required
2            Supplier                               Required
3            General account                        Not used

Bank operations
Each line is a movement with an Amount . For general lines
( Type 3), an optional Tax object holds the VAT
breakdown. The tax amount must be included in the line
amount.
JSON
               Bank, financial & miscellaneous operations

{
"FolderId": "83f26e75-f474-4b09-a1d3-
aa698e18fbf0",
"DaybookId": "87f48c7e-54d1-48d2-aed7-
447e6003bc67",
"Number": 202211001,
"Date": "2022-11-04T00:00:00+00:00",
"Lines": [
{
"Type": 1,
"Account": "400000",
"CompanyId": "32ebe925-23cc-4a3e-8b36-
8b2b33780fc1",
"Amount": 1210,
"Comment": "Payment invoice 2022-10-015",
"Date": "2022-11-04T00:00:00+00:00"
}
]
}

A bank operation can be attached to its source file, such as a
CODA statement ( "FileName": "my-coda.cod" ).

Financial operations
Financial operations work like bank operations, in a daybook
of type Financial (e.g. credit card statements).

Miscellaneous operations (OD)
Miscellaneous operations use debit/credit lines, and the
sum of debits and credits must be balanced:
              Bank, financial & miscellaneous operations

JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-
aa698e18fbf0",
"DaybookId": "c2a1f3e4-7b8d-4e5f-a6b7-
c8d9e0f1a2b3",
"Number": 201909001,
"Date": "2019-09-04T00:00:00+00:00",
"Lines": [
{ "Type": 3, "Account": "499000", "Debit":
1000, "Credit": 0, "Comment":
"Reclassification" },
{ "Type": 3, "Account": "604000", "Debit":
0, "Credit": 1000, "Comment":
"Reclassification" }
]
}

Lines can also carry a MatchNo , a VehicleId and
analytics ( CostLines or CostDistributionKey ).
Updating and deleting
Need         Endpoint                                     Notes
                                       Returns a
Replace                                                   new book
the          book-
                                       entry Id. The
whole        entries.miscellaneous-
                                       original
operation    operations.update
                                       attachment
                                       is deleted.

                Bank, financial & miscellaneous operations

Need         Endpoint                                      Notes
                                         Debit and
                                         credit
Change                                                     amounts
some
book-
                                         cannot be
lines only
entries.miscellaneous-
                                         changed.
operations.lines.update
                                         Partial
                                         update rule
                                         applies.
                                         Only for
book-                                        unconfirmed
Delete       entries.miscellaneous-                        entries
operations.delete                             created
( DELETE )                                    through the
                                         API.

Numbering
Number     is the operation number associated with the book
entry; it can be 0 while the entry is not confirmed. If you set
Confirmed: true , you can let Horus generate the number
with AutoGenerateNumber: true (leave Number at 0 ).
📘 Bank and financial updates
As with invoices and miscellaneous operations,
book-entries.banks.update and book-
entries.financials.update return the newly

                 Bank, financial & miscellaneous operations

generated book entry's Id and delete the original
attachment.

Posting sales &                                       Documents & 

purchase invoices                                      attachments


==================================================================
## GUIDE: Documents & attachments
==================================================================
Documents & attachments
Upload files for automatic processing, attach them to entries, or
store them in the library.

    📘 Conventions
      In the examples, $API_URL stands for the api_url of the connected
      license and $ACCESS_TOKEN for a valid access token. See Quickstart.

The API offers three ways to send files to Horus Office, depending on what should
happen with them:
    Goal                                 Endpoint
    Let Horus process the                documents.new
ATA                     document automatically
                            Documents & attachments

Goal                          Endpoint
rs              into a book entry
ces             Send structured data and       invoices.*.new , book-entries.*.new
s operations    the document in one call      (with multipart/form-data )
Attach a document to an        book-entries.documents.new , book-
existing book entry           entries.documents.annexes.new

Store a document in the
folder's library, without any library.documents.new
book entry

Supported file types
Pdf, Xml, CODA, SODA, and images ( .jpg , .jpeg , .png ).

Uploading with multipart/form-data
All uploads use the multipart/form-data content type with two fields:
Field     Content
file     The file's bytes.
      The JSON-formatted request, the same object as the
       application/json version of the endpoint.
body

Always set FileName in the JSON body, including the extension.
                         Documents & attachments

Bash
curl -X POST "$API_URL/documents.new" \
-H "Authorization: Bearer $ACCESS_TOKEN" \
-F "file=@supplier-invoice.pdf" \
-F 'body={"FolderId":"83f26e75-f474-4b09-a1d3-
aa698e18fbf0","FileName":"supplier-invoice.pdf","Remark":"Invoice
230601"}'

C#
using var form = new MultipartFormDataContent();
form.Add(new ByteArrayContent(File.ReadAllBytes("supplier-
invoice.pdf")), "file", "supplier-invoice.pdf");
form.Add(new StringContent(JsonSerializer.Serialize(new {
FolderId = folderId,
FileName = "supplier-invoice.pdf",
Remark = "Invoice 230601"
})), "body");

var response = await http.PostAsync($"{apiUrl}/documents.new",
form);

Automatic processing: documents.new
documents.new      inserts a document that is processed automatically and
transformed into a book entry. This is the simplest option when you only have
the file, such as a scanned purchase invoice.

                         Documents & attachments

Field                       Description
FolderId                   Required.
FileName                   Required, with extension.
UserComment                Comment from the client for the accountant.
Remark                     Free remark, e.g. the invoice reference.
VehicleId                  Related vehicle, if any.
The response contains the generated document Id. Use documents.info and
documents.list to follow it.

Attaching to existing book entries
Endpoint                                      When
                                      The entry has no document yet.
book-entries.documents.new                   Fails if a main document already
                                      exists.
                                      The entry already has a main
book-
                                      document; adds an annex. Fails if
entries.documents.annexes.new
                                      there is no main document yet.
JSON
{ "BookEntryId": "5b1e8a4c-3d2f-4e6a-9c7b-1f0d2e3a4b5c",
"FileName": "my-invoice.pdf" }

           Library documents
     Documents & attachments

Library documents are stored in the folder's library and are not linked to any
book entry: VAT returns, administrative or social documents, accounting reports,
bank documents, permanent folder…
JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"Title": "VAT return Q3 2024",
"Category": "Vat",
"FileName": "vat-q3-2024.pdf",
"KeyWords": ["vat", "2024"],
"ReferenceDateMonth": 9,
"ReferenceDateYear": 2024
}

Categories: Undefined , Vat , Admin , Social , AccountReport , Bank ,
PermanentFolder .

Action          Endpoint
List / get        library.documents.list   , library.documents.info
Download          library.documents.download

Delete            library.documents.delete

Downloading documents
                           Documents & attachments

documents.download       and library.documents.download return the raw bytes
of the file, not JSON. Read the response as a binary stream.

Bank, financial &                             Outstanding items & matching 

miscellaneous operations


==================================================================
## GUIDE: Outstanding items & matching
==================================================================
Outstanding items & matching
Read open items and match payments with invoices.

Matching links entry lines that offset each other, typically an invoice and its
payment(s), by giving them the same matching number ( MatchNo ). Lines that
are not matched yet make up the outstanding items.

Reading outstanding items
   Need                                     Endpoint
   A customer's outstanding
   debts                                     customers.outstanding

   A supplier's outstanding
   debts                                     suppliers.outstanding

                           Outstanding items & matching

Need                                      Endpoint
rs              Open sales invoices / credit
ces             notes and their linked                    invoices.sales.outstanding.list

s operations    payments
One open sales invoice and
its linked elements (partial              invoices.sales.outstanding.info
payments…)
Unmatched lines of any                    account-histories.list   with
account                                   NotMatchedOnly: true

invoices.sales.outstanding.info               requires the FolderId and one of:
the BookEntryId , or
the BookEntryNumber , formatted as {DaybookSearchKey}-{Number} (e.g.
 VEN-202409001 ).

Matching lines
matching   matches a set of account history lines under one matching number.
JSON
{
"FolderId": "83f26e75-f474-4b09-a1d3-aa698e18fbf0",
"AutoGenerateMatchNo": true,
"AccountHistoryIds": [
  "4f6a2c1e-8b3d-4a7e-9f0c-2d5b8e1a6c3f",
  "7e2b9d4a-1c6f-4e8b-a3d5-0f9c2b7e4a1d"
                      Outstanding items & matching

]
}

JSON
{ "Data": { "MatchNo": 15 } }

Rules:
all lines must have the same account type: 100 Customer, 200 Supplier or
300 General;

for customers and suppliers ( 100 / 200 ), all lines must belong to the same
company;
for general accounts ( 300 ), all lines must belong to the same account.
Choosing the matching number
Either let the API generate it with AutoGenerateMatchNo: true , or provide your
own MatchNo . To get the next free number beforehand, use:
Account type                        Endpoint
Customer                             matching.next-number.customer

Supplier                             matching.next-number.supplier

General account                      matching.next-number.account

📘 Matching at creation time
                        Outstanding items & matching

Invoices and operation lines accept a MatchNo when they are created.
Combined with matching.next-number.* , this lets you post a payment
already matched with its invoice.

Typical flow: reconcile a customer payment
1. Find the open invoice with invoices.sales.outstanding.list (filter on
CompanyIds ).

2. Post the payment with book-entries.banks.new on the customer's
account.
3. Retrieve the account history lines of the invoice and the payment ( account-
histories.list with CompanyId and NotMatchedOnly: true ).

4. Call matching with both line Ids.

   Documents & attachments                                     Testing the API 


==================================================================
## GUIDE: Testing the API
==================================================================
Testing the API
Try endpoints from the API Reference or with our Postman
collection.

You can explore the API without writing any code, either directly from the API
Reference or with Postman. Both need the same two things:
 What                             How to get it
 The api_url of a                 Returned at the end of the authorization flow. It is
 license                          different for every license.
 A valid access token for         Obtained by exchanging the authorization code.
 that license                     It expires after 1 hour.

ATA                  🚧 You are working on real data
                                  Testing the API

 Requests run against the license's real database. Use a test license or a
rs                   test folder for write operations ( .new , .update , .delete ).
Getting a first token quickly
The quickest way is the Postman collection described below: it exchanges the
code and stores the tokens for you. Alternatively, follow steps 1 to 4 of the
Quickstart with curl.
In both cases, you can get the authorization code without a working callback
page: open the authorization URL in your browser and log in. Even if the redirect
page fails to load, the address bar shows the full redirect URL, from which you
can copy code and api_url . The code is valid for 2 minutes.

From the API Reference
Every endpoint in the API Reference can be called from your browser with the Try
It button.
1. Set the API URL. The server URL is a variable named apiUrl . Replace the
 default value https://enter-your-api-url.invalid with your license's
  api_url . This default is deliberately invalid: requests fail until you replace it.

2. Enter the access token in the authentication field.
3. Send the request. Parameters and bodies are pre-filled with examples: adapt
 the identifiers ( FolderId , CompanyId …) to data that exists in your license.

With Postman
Testing the API

The Horus Postman collection contains every endpoint, organised like the API
Reference, with example bodies and responses.
Download the Postman collection
1. Import and configure
Import the file in Postman (Import), then open the collection's Variables tab:
Variable                          Value
               The license's api_url . Required: requests are
apiUrl
               blocked while it is empty.
clientId   ,                     Your integration's credentials.
clientSecret

               One of the redirect URLs registered for your
redirectUri
               integration.

🚧 Keep your secret out of shared workspaces
If you share the collection with your team, store clientSecret in a
Postman environment or vault rather than in the collection itself.

2. Get your tokens
1. Open the authorization URL in your browser (see Quickstart, step 1).
                   Testing the API

2. After login, copy code and api_url from the redirect URL into the
authorizationCode and apiUrl variables.

3. Run Authentication › Exchange authorization code within 2 minutes. The
access and refresh tokens are saved automatically in the collection variables.
3. Call the API
Every request of the collection sends the access token as a Bearer token. When it
expires, after 1 hour, run Authentication › Refresh access token.

📘 Sending files from Postman
Requests that accept a document are pre-filled with a JSON body. To
attach a file, switch the body to form-data, add a file field of type File
with your file, and a body field of type Text containing the JSON.

   Outstanding items & matching                         Changes & versioning 


==================================================================
## GUIDE: Changes & versioning
==================================================================
Changes & versioning
Our backwards-compatibility policy and what counts as a
breaking change.

Our goal is to keep the API backwards-compatible for as long as possible. If
breaking changes must occur, they are announced here, and all integrators are
notified by email in advance.

Backwards-compatible changes
The following changes can happen at any time, without notice. Make sure your
integration tolerates them:
 adding new API endpoints;
 adding new optional parameters to existing API requests;
ATA                  adding new properties to existing API responses;
                              Changes & versioning

adding new webhook types;
rs                 making existing parameters optional;
ces                changing the order of properties in existing API responses;
s operations       fixing bugs that made an endpoint unusable (HTTP 500 errors).

📘 Build tolerant clients
Ignore unknown properties when deserialising responses, and do not rely
on property order.

Breaking changes
The following changes are considered breaking, or backwards-incompatible, and
are always announced in advance:
renaming or removing an endpoint;
renaming or removing a parameter of API requests;
renaming or removing a property of API responses;
changing the format of a parameter of API responses (e.g. integer to float);
making validation of a parameter more strict (e.g. making it required);
returning a different HTTP status code.

Changelog
Announced and past breaking changes are listed in the Changelog.
                         Changes & versioning

   Testing the API                                            Support & FAQ 

```
