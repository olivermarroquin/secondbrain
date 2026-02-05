# Quick Start - Java-Playwright Enhanced

## ⚡ 3-Minute Setup

```bash
# 1. Install dependencies
mvn clean install -DskipTests

# 2. Install browsers
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="install"

# 3. Run tests
mvn test -Dtest=CBAPSEndToEndTests

# 4. View reports
open target/extent-reports/extent-report-*.html
```

## 🎯 What's New

- **60+ PlaywrightManager methods** (was ~25)
- **15-22 methods per page object** (was 5-8)
- **6+ test scenarios** per app (was 2)
- **REST Assured** API testing (NEW!)
- **Parallel execution** (NEW!)
- **Type-safe models** (NEW!)

## 📚 Key Files

- `README.md` - Complete guide (20 pages)
- `ENHANCEMENTS_GUIDE.md` - What was added
- `src/.../EnhancedPlaywrightManager.java` - 60+ methods
- `src/.../pages/RequisitionPage.java` - 22 methods
- `src/.../tests/CBAPSEndToEndTests.java` - 6 scenarios
- `src/.../api/CBAPS_APITests.java` - API tests

## 🚀 Run Commands

```bash
# All tests
mvn test

# Specific test
mvn test -Dtest=CBAPSEndToEndTests#completeWorkflowTest

# Different browser
mvn test -Dbrowser=firefox

# Headless mode
mvn test -Dheadless=true

# API tests
mvn test -Dtest=CBAPS_APITests

# Parallel execution
mvn test -DsuiteXmlFile=testng-parallel.xml
```

## 🎉 You're Ready!

Your framework now matches TypeScript and Selenium versions in robustness!
