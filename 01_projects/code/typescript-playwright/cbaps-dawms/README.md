# CBAPS and DAWMS Automation Framework - TypeScript + Playwright

**Professional-grade automation framework** for CBAPS and DAWMS applications, built with **TypeScript** and **Playwright Test** using the **Page Object Model** pattern.

## 📁 Project Structure

```
typescript-automation/
├── package.json                      # Dependencies and scripts
├── tsconfig.json                     # TypeScript configuration
├── playwright.config.ts              # Playwright Test configuration
│
├── cbaps/                           # CBAPS Automation Framework
│   ├── library/
│   │   ├── types.ts                 # TypeScript interfaces and types
│   │   ├── BaseTest.ts              # Base test class with fixtures
│   │   └── PlaywrightManager.ts     # Enhanced Playwright wrapper
│   ├── pages/
│   │   ├── PortalHomePage.ts
│   │   ├── CBAPSDashboardPage.ts
│   │   ├── RequisitionPage.ts
│   │   ├── FundingLinesPage.ts
│   │   ├── RoutingApprovalPage.ts
│   │   └── StatusTrackerPage.ts
│   └── tests/
│       └── cbaps.end-to-end.spec.ts  # Comprehensive test scenarios
│
└── dawms/                           # DAWMS Automation Framework
    ├── library/
    │   ├── types.ts
    │   ├── BaseTest.ts
    │   └── PlaywrightManager.ts
    ├── pages/
    │   ├── PortalHomePage.ts
    │   ├── DAWMSDashboardPage.ts
    │   ├── SubmissionIntakePage.ts
    │   ├── ReviewerAssignmentPage.ts
    │   ├── SignatureRoutingPage.ts (in ReviewerAssignmentPage.ts)
    │   └── MilestoneStatusPage.ts
    └── tests/
        └── dawms.end-to-end.spec.ts  # Comprehensive test scenarios
```

## 🎯 Key Features

### ✅ TypeScript Benefits
- **Strong typing** with interfaces and types
- **Better IDE support** with IntelliSense and autocomplete
- **Compile-time error detection**
- **Enhanced refactoring capabilities**
- **Self-documenting code** with type annotations

### ✅ Enhanced Page Object Model
- **Type-safe** page objects with interfaces
- **Comprehensive validation methods**
- **Fluent API** with method chaining
- **Business-level method names**
- **Automatic page stability checks**
- **Enhanced error handling**

### ✅ Robust Test Scenarios
- **Multiple test cases** per workflow
- **Positive and negative testing**
- **Form validation tests**
- **Data validation** at each step
- **Metrics verification**
- **Search functionality testing**
- **Draft save/resume workflows**

### ✅ Advanced Features
- **Screenshot on failure** (automatic)
- **Video recording** (configurable)
- **Trace files** for debugging
- **Multiple browser support** (Chromium, Firefox, WebKit)
- **Parallel execution** support
- **HTML/JSON/JUnit reporters**
- **Retry on failure** (configurable)

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Basic TypeScript knowledge

### Installation

```bash
# Install dependencies
npm install

# Install Playwright browsers
npx playwright install

# Compile TypeScript (optional - tests run directly)
npm run compile
```

### Running Tests

```bash
# Run all tests
npm test

# Run CBAPS tests only
npm run test:cbaps

# Run DAWMS tests only
npm run test:dawms

# Run in headed mode (see browser)
npm run test:headed

# Run in debug mode
npm run test:debug

# Run with Playwright UI mode
npm run test:ui

# Show HTML report
npm run report
```

### Running Specific Tests

```bash
# Run specific test file
npx playwright test cbaps/tests/cbaps.end-to-end.spec.ts

# Run specific test by name
npx playwright test -g "Complete CBAPS workflow"

# Run tests in specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run with specific workers (parallel)
npx playwright test --workers=4
```

## 📝 CBAPS Workflow

**Business Flow:** Requisition Creation → Funding Lines → Approval Routing → Status Tracking

### Test Scenarios Covered

1. **Complete CBAPS workflow** - Full end-to-end with all steps
2. **Single funding line workflow** - Simplified flow
3. **Draft save and resume** - Save draft, validate metadata
4. **Form validation tests** - Empty form and partial validation
5. **Funding calculations** - Complex multi-line calculations
6. **Dashboard metrics** - Metrics verification and search

### Example Test Code

```typescript
test('Complete CBAPS workflow', async ({ testPage, pwManager }) => {
  // Portal → CBAPS Dashboard
  const portal = new PortalHomePage(testPage, pwManager);
  await portal.navigateToPortal(PORTAL_URL);
  
  const dashboard = await portal.openCBAPS();
  const isDashboardValid = await dashboard.validateDashboardLoaded();
  expect(isDashboardValid).toBeTruthy();

  // Create Requisition
  const reqPage = await dashboard.goToCreateRequisition();
  const requisitionData: RequisitionData = {
    title: `FY26 Cloud Infrastructure - ${TestUtils.timestamp()}`,
    fundType: FundType.Operations,
    priority: 'High'
  };
  
  await reqPage.createRequisition(requisitionData);

  // Add Funding Lines
  const fundingPage = await reqPage.goToFundingLines();
  const fundingLines: FundingLineData[] = [
    { amount: '25000', fiscalYear: '2026', category: 'Infrastructure' },
    { amount: '15000', fiscalYear: '2026', category: 'Software' }
  ];
  
  await fundingPage.addMultipleFundingLines(fundingLines);
  const total = await fundingPage.getTotalAmount();
  expect(total).toBe(40000);

  // Route for Approval
  const routingPage = await fundingPage.continueToRouting();
  const statusPage = await routingPage.submitForApproval('Branch Chief');

  // Validate Final Status
  const status = await statusPage.validateStatus(RequisitionStatus.Submitted);
  expect(status).toBeTruthy();
});
```

## 🧬 DAWMS Workflow

**Business Flow:** Submission Intake → Reviewer Assignment → Signature Routing → Milestone Tracking

### Test Scenarios Covered

1. **Complete DAWMS workflow** - Full end-to-end with multiple reviewers
2. **Single reviewer workflow** - Simplified assignment flow
3. **Draft save workflow** - Save submission as draft
4. **Form validation tests** - Empty and partial validation
5. **Multiple reviewer validation** - Complex reviewer assignments
6. **Dashboard search** - Search and metrics functionality
7. **Step-by-step validation** - Validation at each workflow step

### Example Test Code

```typescript
test('Complete DAWMS workflow', async ({ testPage, pwManager }) => {
  // Portal → DAWMS Dashboard
  const portal = new PortalHomePage(testPage, pwManager);
  await portal.navigateToPortal(PORTAL_URL);
  
  const dashboard = await portal.openDAWMS();

  // Create Submission
  const intakePage = await dashboard.goToSubmissionIntake();
  const submissionData: SubmissionData = {
    submissionType: SubmissionType.NDA,
    applicationNumber: `NDA-${TestUtils.randomNumber(100000, 999999)}`,
    sponsorName: 'PharmaTech Inc.',
    drugName: 'TestDrug'
  };
  
  const assignmentPage = await intakePage.createSubmission(submissionData);

  // Assign Multiple Reviewers
  const reviewers: ReviewerData[] = [
    { role: 'Clinical Reviewer', name: 'Dr. Jane Smith' },
    { role: 'Pharmacologist', name: 'Dr. John Doe' }
  ];
  
  await assignmentPage.assignMultipleReviewers(reviewers);
  expect(await assignmentPage.getReviewerCount()).toBe(2);

  // Route for Signature
  const signaturePage = await assignmentPage.routeToSignatureStep();
  const statusPage = await signaturePage.submitForSignature('Division Director');

  // Validate Milestone and Status
  const workflowValid = await statusPage.validateWorkflow(
    SubmissionStatus.PendingSignature,
    MilestoneType.SignatureRouting
  );
  expect(workflowValid).toBeTruthy();
});
```

## 🔧 Framework Components

### TypeScript Types and Interfaces

```typescript
// Strong typing for requisition data
interface RequisitionData {
  title: string;
  fundType: string;
  description?: string;
  priority?: 'Low' | 'Medium' | 'High' | 'Critical';
}

// Enum for requisition status
enum RequisitionStatus {
  Draft = 'Draft',
  Submitted = 'Submitted',
  InReview = 'In Review',
  Approved = 'Approved',
  Rejected = 'Rejected'
}

// Validation result type
interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings?: string[];
}
```

### PlaywrightManager (Enhanced Wrapper)

```typescript
class PlaywrightManager {
  // Type-safe click with retry
  async click(locator: Locator, options?: { timeout?: number }): Promise<void>
  
  // Type with validation
  async type(locator: Locator, text: string, options?: { clear?: boolean }): Promise<void>
  
  // Wait with custom message
  async waitVisible(selector: string, message?: string): Promise<void>
  
  // Dropdown selection with validation
  async selectDropdown(locator: Locator, value: string): Promise<void>
  
  // Get text content
  async getText(locator: Locator): Promise<string>
  
  // Visibility checks
  async isVisible(locator: Locator): Promise<boolean>
  async isEnabled(locator: Locator): Promise<boolean>
  
  // Screenshots
  async screenshot(name: string, fullPage?: boolean): Promise<string>
  async screenshotBase64(): Promise<string>
  
  // Navigation
  async navigateTo(url: string, waitUntil?: 'load' | 'networkidle'): Promise<void>
}
```

### Page Object Pattern

```typescript
class RequisitionPage {
  readonly page: Page;
  readonly pwManager: PlaywrightManager;
  
  // Locators defined as readonly
  readonly titleInput: Locator;
  readonly fundTypeDropdown: Locator;
  readonly submitButton: Locator;

  constructor(page: Page, pwManager: PlaywrightManager) {
    // Initialize locators
    // Add stability anchor
    this.pwManager.waitVisible('#requisitionTitle');
  }

  // Business-level method that returns next page
  async createRequisition(data: RequisitionData): Promise<void> {
    await this.pwManager.type(this.titleInput, data.title);
    await this.pwManager.selectDropdown(this.fundTypeDropdown, data.fundType);
    await this.pwManager.click(this.submitButton);
  }

  // Navigation returns next Page Object
  async goToFundingLines(): Promise<FundingLinesPage> {
    await this.pwManager.click(this.goToFundingLink);
    return new FundingLinesPage(this.page, this.pwManager);
  }

  // Validation method
  async validateForm(): Promise<ValidationResult> {
    const errors: string[] = [];
    // Validation logic
    return { isValid: errors.length === 0, errors };
  }
}
```

### Test Utils

```typescript
class TestUtils {
  static logStep(step: string): void
  static logSuccess(message: string): void
  static logInfo(message: string): void
  static logWarning(message: string): void
  static logError(message: string): void
  
  static randomEmail(): string
  static randomString(length: number): string
  static randomNumber(min: number, max: number): number
  static timestamp(): string
  
  static formatCurrency(amount: number): string
  static waitFor(ms: number, reason?: string): Promise<void>
  
  // Retry with exponential backoff
  static async retryAction<T>(
    action: () => Promise<T>,
    maxRetries?: number
  ): Promise<T>
}
```

## 📊 Reporting

### HTML Report (Default)
```bash
# Run tests
npm test

# View report
npm run report
```

### JSON Report
Located at: `test-results/results.json`

### JUnit Report (CI/CD)
Located at: `test-results/junit.xml`

### Console Output
Real-time test execution with emojis:
- ✅ Success messages
- ❌ Error messages
- ⚠️  Warning messages
- ℹ️  Info messages
- 📋 Step descriptions

## 📹 Artifacts

### Screenshots
- **Location**: `test-results/`
- **Trigger**: Automatic on failure
- **Format**: PNG

### Videos
- **Location**: `test-results/`
- **Trigger**: Retained on failure
- **Format**: WebM

### Traces
- **Location**: `target/traces/`
- **Trigger**: On first retry
- **View**: `npx playwright show-trace trace.zip`

## 🔍 Debugging

### Playwright Inspector
```bash
# Debug specific test
npx playwright test --debug cbaps/tests/cbaps.end-to-end.spec.ts

# Debug with headed browser
npx playwright test --headed --debug
```

### UI Mode (Interactive)
```bash
npm run test:ui
```

### VSCode Debugging
Add to `.vscode/launch.json`:
```json
{
  "type": "node",
  "request": "launch",
  "name": "Playwright Test",
  "program": "${workspaceFolder}/node_modules/@playwright/test/cli.js",
  "args": ["test", "--headed"],
  "console": "integratedTerminal"
}
```

## ⚙️ Configuration

### Browser Configuration
Edit `playwright.config.ts`:
```typescript
projects: [
  { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  { name: 'webkit', use: { ...devices['Desktop Safari'] } }
]
```

### Timeouts
```typescript
use: {
  actionTimeout: 30000,       // 30 seconds
  navigationTimeout: 60000,   // 60 seconds
},
timeout: 120000,              // 2 minutes per test
```

### Retries
```typescript
retries: process.env.CI ? 2 : 0,  // Retry twice on CI
```

## 🔄 CI/CD Integration

### GitHub Actions
```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## 🎓 Best Practices Implemented

1. **Type Safety** - All methods have proper TypeScript types
2. **Stability Anchors** - Every page waits for key elements
3. **Method Chaining** - Fluent APIs for better readability
4. **Comprehensive Validation** - Multiple validation methods per page
5. **Error Handling** - Try-catch with meaningful error messages
6. **Logging** - Detailed console logging at each step
7. **Screenshots/Videos** - Automatic capture on failures
8. **Page Object Returns** - Each action returns next page object
9. **Business-Level Methods** - No raw Playwright in tests
10. **Multiple Scenarios** - Positive, negative, and edge cases

## 🔗 Differences from Java/Python Versions

| Feature | Java/TestNG | Python/pytest | TypeScript/Playwright |
|---------|-------------|---------------|----------------------|
| **Language** | Java | Python | TypeScript |
| **Framework** | TestNG | pytest | Playwright Test |
| **Typing** | Strong (static) | Dynamic (optional) | Strong (static) |
| **Annotations** | @Test, @BeforeClass | fixtures | fixtures |
| **Naming** | camelCase | snake_case | camelCase |
| **Page Objects** | Classes | Classes | Classes with types |
| **Assertions** | AssertJ | pytest assert | expect() |

## 📚 Additional Resources

- [Playwright TypeScript Docs](https://playwright.dev/docs/test-typescript)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)

---

**Framework Version**: 1.0.0  
**Created**: February 2026  
**Technologies**: TypeScript, Playwright Test, Node.js  
**Pattern**: Page Object Model (POM)  
**Applications**: CBAPS, DAWMS
