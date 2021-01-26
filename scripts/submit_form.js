// Google Apps Script to submit a form to a Google Sheet and send an email notification

var SCRIPT_PROPERTIES = PropertiesService.getScriptProperties();
const EMAIL_ADDRESS = "";  // set this!

const formIdToNameMap = new Map([
  ["feedback", "Give Feedback"],
  ["report_missing_info", "Report Missing or Outdated Information"],
  ["partner_with_freefrom", "Partner with FreeFrom"],
  ["build_collective_survivor_power", "Build Collective Survivor Power"],
  ["policy_ideas", "Share your Policy Ideas"],
]);

function setup() {
  var doc = SpreadsheetApp.getActiveSpreadsheet();
  SCRIPT_PROPERTIES.setProperty("key", doc.getId());
}

function doPost(request) {
  const { _, postData: { contents, type } = {} } = request;

  if (type !== "application/json") {
    return ContentService.createTextOutput(
      JSON.stringify({
        result: "error",
        error: "expected type application/json",
      })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  const data = JSON.parse(contents);
  return submitForm(flattenArrays(data));
}

// turns arrays into a string of comma-separated values
function flattenArrays(data) {
  for (var key in data) {
    if (Array.isArray(data[key])) {
      data[key] = data[key].join(", ");
    }
  }
  return data;
}

function submitForm(data) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000); // wait 10 seconds before conceding defeat

  try {
    var doc = SpreadsheetApp.openById(SCRIPT_PROPERTIES.getProperty("key"));
    var formId = data["form"];
    var formName = formIdToNameMap.get(formId);
    var sheet = doc.getSheetByName(formName);

    // question keys are on the first row
    var questions = sheet
      .getRange(1, 1, 1, sheet.getLastColumn())
      .getValues()[0];

    // friendly question names are on the second row
    var questionsFriendly = sheet
      .getRange(2, 1, 2, sheet.getLastColumn())
      .getValues()[0];

    // get next empty row
    var nextRow = sheet.getLastRow() + 1;
    var row = [];
    var submitted = { form: formId };

    // loop through the form questions
    var question, response;
    for (question of questions) {
      if (question === "submitted_at") {
        response = new Date();
      } else {
        response = question in data ? data[question] : "";
      }
      row.push(response);
      submitted[question] = response;
    }
    sheet.getRange(nextRow, 1, 1, row.length).setValues([row]);

    return ContentService.createTextOutput(
      JSON.stringify(submitted)
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (e) {
    return ContentService.createTextOutput(
      JSON.stringify({ result: "error", description: e })
    ).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();

    // this needs to happen after the first lock is released
    notifyFreeFrom(formName, questions, questionsFriendly, data);
  }
}

function notifyFreeFrom(formName, questions, questionsFriendly, data) {
  htmlBody = `Hi FreeFrom Staff,<br><br> A new submission to the ${formName} form has been made!<br><br>`;
  var i, response;
  for (i in questions) {
    if (questions[i] === "submitted_at") continue;
    response = questions[i] in data ? data[questions[i]] : "[not answered]";
    htmlBody = htmlBody.concat(
      `<b>${questionsFriendly[i]}</b><br> ${response}<br><br>`
    );
  }
  MailApp.sendEmail({
    to: EMAIL_ADDRESS,
    subject: `New form submission on ${formName}`,
    htmlBody: htmlBody,
  });
}
