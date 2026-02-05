# CBAPS and DAWMS Automation Framework - Refactored

This is the refactored automation framework for **CBAPS** and **DAWMS** applications, built using Java + Playwright + TestNG with the Page Object Model (POM) pattern.

## 📁 Project Structure

```
com/
├── cbaps/
│   ├── library/
│   │   ├── Base.java                      # TestNG base class - lifecycle management
│   │   ├── PlaywrightManager.java         # Playwright wrapper - browser interactions
│   │   ├── ExtentReportManager.java       # Singleton for HTML reporting
│   │   └── ExcelManager.java              # Excel data reader for data-driven tests
│   ├── pages/
│   │   ├── PortalHomePage.java            # Portal entry point
│   │   ├── CBAPSDashboardPage.java        # CBAPS main dashboard
│   │   ├── RequisitionPage.java           # Requisition creation
│   │   ├── FundingLinesPage.java          # Funding lines management
│   │   ├── RoutingApprovalPage.java       # Approval routing
│   │   └── StatusTrackerPage.java         # Status validation
│   └── tests/
│       └── CBAPS_EndToEnd_Test.java       # Complete CBAPS workflow tests
│
└── dawms/
    ├── library/
    │   ├── Base.java                      # TestNG base class - lifecycle management
    │   ├── PlaywrightManager.java         # Playwright wrapper - browser interactions
    │   ├── ExtentReportManager.java       # Singleton for HTML reporting
    │   └── ExcelManager.java              # Excel data reader for data-driven tests
    ├── pages/
    │   ├── PortalHomePage.java            # Portal entry point
    │   ├── DAWMSDashboardPage.java        # DAWMS main dashboard
    │   ├── SubmissionIntakePage.java      # Drug submission intake
    │   ├── ReviewerAssignmentPage.java    # Reviewer assignment
    │   ├── SignatureRoutingPage.java      # Signature routing
    │   └── MilestoneStatusPage.java       # Milestone & status validation
    └── tests/
        └── DAWMS_EndToEnd_Test.java       # Complete DAWMS workflow tests
```

## 🎯 Key Design Principles

### 1. **Page Object Model (POM)**
- **Locators** and **page-specific actions** are defined inside **Page Object classes**
- Each application screen has a single source of truth for its UI elements and behaviors
- Page Objects return the next Page Object to enforce workflow sequencing

### 2. **Composition-Based Architecture**
- **Base** manages **lifecycle** and **orchestration** (TestNG annotations)
- **PlaywrightManager** manages **browser interactions** (Playwright wrapper)
- **Page Objects** encapsulate **UI structure** and **business behavior**

### 3. **Test Readability**
- Tests read like real business workflows, not UI scripts
- Example: `Portal → Dashboard → Requisition → Funding → Routing → Status`
- Each step returns the next page object naturally

### 4. **Separation of Concerns**
- **Tests** extend Base for lifecycle management
- **Base** owns PlaywrightManager instance
- **PlaywrightManager** owns Playwright/Browser/Context/Page
- **Page Objects** use PlaywrightManager helpers + Page instance

## 🚀 CBAPS Workflow

**Business Flow:** Requisition Creation → Funding Lines → Approval Routing → Status Tracking

```java
// Portal → CBAPS Dashboard
PortalHomePage portal = new PortalHomePage(page, pwm);
portal.navigateToPortal("https://cbaps-portal.example.com");
CBAPSDashboardPage dashboard = portal.openCBAPS();

// Dashboard → Requisition
RequisitionPage reqPage = dashboard.goToCreateRequisition();
reqPage.createRequisition("FY26 Cloud Tools", "Operations");

// Requisition → Funding Lines
FundingLinesPage fundingPage = reqPage.goToFundingLines();
fundingPage.addFundingLine("5000");

// Funding → Routing
RoutingApprovalPage routingPage = fundingPage.continueToRouting();

// Routing → Status
StatusTrackerPage statusPage = routingPage.submitForApproval("Branch Chief");

// Validation
assertThat(statusPage.getStatus()).isEqualTo("Submitted");
```

## 🧪 DAWMS Workflow

**Business Flow:** Submission Intake → Reviewer Assignment → Signature Routing → Milestone Tracking

```java
// Portal → DAWMS Dashboard
PortalHomePage portal = new PortalHomePage(page, pwm);
portal.navigateToPortal("https://dawms-portal.example.com");
DAWMSDashboardPage dashboard = portal.openDAWMS();

// Dashboard → Submission Intake
SubmissionIntakePage intake = dashboard.goToSubmissionIntake();

// Intake → Reviewer Assignment
ReviewerAssignmentPage assignment = intake.createSubmission("NDA", "123456");

// Assignment → Signature Routing
SignatureRoutingPage signature = assignment
    .assignReviewer("Clinical Reviewer", "Jane Doe")
    .routeToSignatureStep();

// Signature → Milestone/Status
MilestoneStatusPage status = signature.submitForSignature("Division Director");

// Validation
assertThat(status.getStatus()).isEqualTo("Pending Signature");
assertThat(status.getMilestone()).isEqualTo("Signature Routing");
```

## 🔧 Key Components

### Base Class
- Manages TestNG lifecycle: `@BeforeSuite`, `@BeforeClass`, `@BeforeMethod`, `@AfterMethod`, `@AfterClass`, `@AfterSuite`
- Initializes ExtentReports for HTML reporting
- Creates PlaywrightManager and Page per test
- Captures screenshots and videos on failure
- Logs steps to ExtentReports

### PlaywrightManager
- Wrapper around Playwright primitives
- Provides common actions: `click()`, `type()`, `waitVisible()`, `selectDropdown()`, `fileUpload()`
- Manages browser/context initialization and teardown
- Handles screenshot capture (full page and Base64)
- Supports demo mode with element highlighting

### Page Objects
- Constructor takes `Page page` and `PlaywrightManager pwm`
- Constructor includes stability anchor (wait for page to be ready)
- Methods represent business actions, not raw UI interactions
- Methods return next Page Object for workflow chaining
- Locators are private fields, actions are public methods

### Tests
- Extend Base class
- Create test node in ExtentReports: `test = extent.createTest("Test Name")`
- Call business-level methods on Page Objects
- Log steps using `addStepToReport()`
- Perform assertions on workflow outcomes

## 📊 Reporting

### ExtentReports
- HTML reports generated in `target/report/`
- CBAPS reports: `cbaps-extent-report-{timestamp}.html`
- DAWMS reports: `dawms-extent-report-{timestamp}.html`
- Dark theme with test timeline, dashboard, and logs
- Screenshots and videos attached on failure

### Logging
- SLF4J with Logback
- Console and file logging
- Log location: `target/logs/automation.log`

## 📹 Artifacts

- **Screenshots**: `target/screenshot/`
- **Videos**: `target/videos/`
- **Reports**: `target/report/`

## 🧩 Common Patterns

### Method Chaining
```java
fundingPage.addFundingLine("5000")
           .addFundingLine("3000")
           .addFundingLine("2000");
```

### Workflow Navigation
```java
// Each method returns next page object
RequisitionPage reqPage = dashboard.goToCreateRequisition();
FundingLinesPage fundingPage = reqPage.goToFundingLines();
RoutingApprovalPage routingPage = fundingPage.continueToRouting();
StatusTrackerPage statusPage = routingPage.submitForApproval("Approver");
```

### Step Reporting
```java
addStepToReport("Step 1: Navigated to portal.");
addStepToReport("Step 2: Created requisition.");
// Shows up in ExtentReports timeline
```

## ⚙️ Configuration

### Browser Settings (in PlaywrightManager)
- **browserType**: "chrome" (default), "firefox", "webkit", "msedge"
- **isHeadless**: false (default) - run in headed mode
- **isMaximized**: true (default) - maximize browser
- **isVideoRecording**: true (default) - record videos
- **isDemoMode**: false (default) - highlight elements

### Lifecycle Management (in Base)
- **Suite-level**: Initialize ExtentReports once
- **Class-level**: Create Playwright + Browser + Context once per class
- **Method-level**: Create new Page per test method (isolation)
- **Teardown**: Capture evidence on failure, close pages, flush reports

## 🎓 Best Practices

1. **Always create stability anchors** in Page Object constructors
   ```java
   pwm.waitVisible("text=Page Title");
   ```

2. **Return next Page Object** to enforce workflow
   ```java
   public FundingLinesPage goToFundingLines() {
       pwm.click(goToFundingLink);
       return new FundingLinesPage(page, pwm);
   }
   ```

3. **Use business-level method names**
   - ✅ `createRequisition(title, fundType)`
   - ❌ `fillTitleField()`, `clickSubmitButton()`

4. **Log every step** for traceability
   ```java
   addStepToReport("Step 5: Added funding line.");
   ```

5. **Validate workflow outcomes**, not just UI elements
   ```java
   assertThat(statusPage.getStatus()).isEqualTo("Submitted");
   ```

## 🔄 Differences from Original Framework

### Package Structure
- **Before**: `com.playwright.week5.library`, `com.playwright.thegreatcourses.pages`
- **After**: `com.cbaps.library`, `com.cbaps.pages`, `com.dawms.library`, `com.dawms.pages`

### Domain Focus
- **Before**: Generic e-commerce examples (The Great Courses, mortgage calculators)
- **After**: CBAPS requisition workflows and DAWMS drug submission workflows

### Page Object Naming
- **Before**: `HomePage`, `CheckOutPage`, `ProductTypePage`
- **After**: `CBAPSDashboardPage`, `RequisitionPage`, `SubmissionIntakePage`

### Test Organization
- **Before**: Single test class per website
- **After**: End-to-end workflow tests per application (CBAPS_EndToEnd_Test, DAWMS_EndToEnd_Test)

## 🚀 Running Tests

### Run CBAPS Tests
```bash
mvn test -Dtest=CBAPS_EndToEnd_Test
```

### Run DAWMS Tests
```bash
mvn test -Dtest=DAWMS_EndToEnd_Test
```

### Run All Tests
```bash
mvn test
```

## 📝 Notes

- The framework preserves the original architecture and design patterns
- PlaywrightManager and Base are adapted but not redesigned
- All utilities (screenshot, video, reporting, Excel) remain functional
- Tests can be extended for parallel execution with ThreadLocal storage

---

**Created**: February 2026  
**Framework**: Java + Playwright + TestNG  
**Pattern**: Page Object Model (POM)  
**Applications**: CBAPS, DAWMS
