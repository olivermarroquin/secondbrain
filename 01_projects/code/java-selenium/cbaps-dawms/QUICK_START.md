# CBAPS & DAWMS Java Selenium Automation - QUICK START

## 🚀 Complete Enterprise Framework

**Production-Ready Java Selenium Framework with:**
✅ REST Assured API Testing
✅ Data-Driven Testing (Excel)
✅ Parallel Execution (TestNG)
✅ ExtentReports
✅ Page Object Model
✅ Enhanced GlobalSelenium (50+ methods)

## 📦 What's Included

- **Enhanced GlobalSelenium**: 50+ methods (all your original + 20 new)
- **REST Assured**: APIHelper for API testing
- **Data-Driven**: ExcelManager for parameterization
- **Parallel Tests**: TestNG XML configurations
- **ExtentReports**: Beautiful HTML reports
- **Comprehensive Tests**: 6+ scenarios per application
- **Enhanced Page Objects**: 15-22 methods each

## ⚡ Quick Setup

```bash
# Navigate to project
cd java-selenium-automation

# Install dependencies
mvn clean install -DskipTests

# Run CBAPS tests
mvn test -Dtest=CBAPSEndToEndTests

# Run DAWMS tests
mvn test -Dtest=DAWMSEndToEndTests

# Run with parallel execution
mvn test -DsuiteXmlFile=testng-parallel.xml

# Run API tests
mvn test -Dtest=CBAPS_APITests

# View reports
open target/extent-reports/extent-report.html
```

##  Complete Framework Structure

The attached ZIP contains everything you need - just extract and run!

**See README.md for complete documentation.**
