- Page Object Model Setup for CBAPS & DAWMS
    
    <aside>
    🎙️
    
    - Main Idea:
        
        **Locators** and **page-specific actions** are defined inside **Page Object classes**, so **each application screen has a single source of truth for its UI elements and behaviors.**
        
        **Test classes** initialize ****these **Page Objects** and call their **business-level methods**, which **allows tests to read like real workflows instead of low-level UI interactions.**
        
        **To avoid duplicating raw Playwright calls**, a **`PlaywrightManager`** acts as a wrapper around Playwright and owns the **Playwright**, **Browser**, **BrowserContext**, and **Page objects**. This manager exposes common actions such as clicking elements, entering text, waiting for visibility, taking screenshots, and handling file uploads, which **Page Objects** reuse **for consistent and stable interactions.**
        
        **Test classes** inherit from a `Base` class, which controls the test lifecycle using **TestNG annotations**. The **Base class** is responsible for initializing the `PlaywrightManager`, creating a fresh **Page** before each test method, and handling teardown logic such as closing pages, capturing screenshots, recording videos, and reporting failures.
        
        Importantly, the **Base class** does not inherit from Playwright. Instead, it **owns an instance** of `PlaywrightManager`, which internally manages Playwright resources. **This composition-based design keeps responsibilities separated**: 
        
        **Base** manages **lifecycle** and **orchestration**
        
        **PlaywrightManager** manages **browser interactions**, and 
        
        **Page Objects** encapsulate **UI structure** and **business behavior**.
        
    - One Liner
        
        Tests extend Base for lifecycle. 
        Base initializes PlaywrightManager. 
        PlaywrightManager creates Playwright/Browser/Context and provides a Page per test. 
        Page Objects store locators and use the shared PlaywrightManager helpers + the Page instance to perform stable business actions.
        
    </aside>
    
    - **Script Broken Down with Code Examples**
        - **Locators** and **page-specific actions** are defined inside **Page Object classes**, so **each application screen has a single source of truth for its UI elements and behaviors.**
            
            <aside>
            🎙️
            
            “**Tests** call **business-workflow methods**; **locators** stay inside the **page object**. That’s how we keep **CBAPS/DAWMS** automation maintainable when UI changes. The **Page** and the **PlaywrightManager** are created during **Base** setup. The **test** then injects them into **Page Objects** via constructors so the **Page Objects** don’t create browsers themselves. We wrap the most common interactions, but **Page Objects** can still call Playwright directly for specialized actions. If dropdowns become common, we promote that into the wrapper for consistency.”
            
            - Each **Page Object class** contains **locators** (`Locator`, selector strings, etc.)
            - It also contains **page-specific actions** (“click submit”, “enter vendor EIN”, “route for approval”)
            
            That’s the POM core rule: **locators + actions are bundled per page.**
            
            **Typical pattern:**
            
            The **test** extends Base, so it has access to those fields (`page`, `pwm`)
            
            The **test passes both** into the **Page Object constructor**
            
            - Page Object constructor takes:
                - `Page page` - **Base** creates a new Playwright **`Page`** in `@BeforeMethod` via `pwm.openNewBrowserPage()`
                - `PlaywrightManager pwm` - **Base** initializes `PlaywrightManager` in `@BeforeClass`
            
            **Example Use in Test:**
            
            ```java
            public class CBAPS_RequisitionTest extends Base {
            	
            	@Test
            	public void testFlow() {
            	    // page + pwm already exist because Base created them in setup
            	    RequisitionPage reqPage = new RequisitionPage(page, pwm);
            	}
            }
            ```
            
            So each Page Object can:
            
            - Use `page` **for direct Playwright-native raw methods directly when needed**
                - That is exactly why Page and Locator are available inside Page Objects
            - Use `pwm` **for shared helper actions** (waits, highlight, file upload, screenshots)
            
            This is also how you make the page object portable and testable.
            
            Below is **true POM end-to-end**: **action returns next page.**
            
            ⭐️ Means there are notes in those toggles
            
            </aside>
            
            - `PortalHomePage` **→ routes to either app dashboard**
                
                <aside>
                🎙️
                
                - Click CBAPS → returns **CBAPSDashboardPage**
                - Click DAWMS → returns **DAWMSDashboardPage**
                - Each Dashboard has:
                    - “Go to Requisition / Create Request” (CBAPS) → returns **RequisitionPage**
                    - “Go to Submission Intake” (DAWMS) → returns **SubmissionIntakePage**
                - Tests show full flow with `addStepToReport(...)` at each stage.
                </aside>
                
                ```java
                public class PortalHomePage {
                
                    private final Page page;
                    private final PlaywrightManager pwm;
                
                    private final Locator cbapsLink;
                    private final Locator dawmsLink;
                
                    public PortalHomePage(Page page, PlaywrightManager pwm) {
                        this.page = page;
                        this.pwm = pwm;
                
                        this.cbapsLink = page.locator("a:has-text('CBAPS')");
                        this.dawmsLink = page.locator("a:has-text('DAWMS')");
                
                        // Stability anchor: portal loaded
                        pwm.waitVisible("text=Application Portal");
                    }
                
                    public CBAPSDashboardPage openCBAPS() {
                        pwm.click(cbapsLink);
                        return new CBAPSDashboardPage(page, pwm);
                    }
                
                    public DAWMSDashboardPage openDAWMS() {
                        pwm.click(dawmsLink);
                        return new DAWMSDashboardPage(page, pwm);
                    }
                }
                ```
                
            - CBAPS Page Objects
                - `CBAPSDashboardPage` **→ goes to** `RequisitionPage`
                    
                    ```java
                    public class CBAPSDashboardPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    		
                    		// Locator for the button that leads to the Requisition Page
                        private final Locator createRequisitionBtn;
                    
                        public CBAPSDashboardPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    				// Initialization for the createRequisitionBtn Locator
                            this.createRequisitionBtn = page.locator("button:has-text('Create Requisition')");
                    
                            pwm.waitVisible("text=CBAPS Dashboard");
                        }
                        
                    		**// This Method -> navigates to the RoutingApprovalPage and returns it**
                        // it passes the same 'page' and 'pwm' that was used in this Page Object for end-to-end testing
                        public RequisitionPage goToCreateRequisition() {
                            pwm.click(createRequisitionBtn);
                            return new RequisitionPage(page, pwm);
                        }
                    }
                    ```
                    
                - `RequisitionPage` **-> returns** `FundingLinesPage` **⭐️**
                    
                    ```java
                    // Typical Imports Include the Following:
                    import org.slf4j.Logger;
                    import org.slf4j.LoggerFactory;
                    import net.datafaker.Faker;   //depending on if fake data is needed in the Page Object
                    
                    import com.microsoft.playwright.Page;
                    import com.microsoft.playwright.options.AriaRole;
                    import com.playwright.cbaps.library.Base;
                    import com.playwright.cbaps.library.PlaywrightManager;
                    
                    public class RequisitionPage {
                    
                    		// Declare the Logger (coming from slf4j)
                    		private static final Logger log = LoggerFactory.getLogger(RequisitionPage.class);
                    
                    		// Declare the Page and PlaywrightManager in each Page Class
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        // Declare Locators: they belong to the page object (single source of truth)
                        private final Locator titleInput;
                        private final Locator fundTypeDropdown;
                        private final Locator submitButton;
                        private final Locator statusBadge;
                        private final Locator goToFundingLink;
                        private final Locator routeForApprovalButton;
                    
                    		/* Constructor:
                    			 to initialize the Page and pwm (PlaywrightManager) coming from my test layer, and ultimately from Base
                    					**Example in Test Class:**	RequisitionPage requisitionPage = new RequisitionPage(page, myPlaywright);
                    					**Example in Base Class:**
                    							@BeforeClass
                    							public void beforeTestClass() {
                    								myPlaywright = new PlaywrightManager();
                    								myPlaywright.initPlaywright(); }
                    							@BeforeMethod
                    							public void setUp() {
                    								page = myPlaywright.openNewBrowserPage(); }
                    		   to initizlize locators once
                    		   to create a constructor wait -> Anchor for 'page is ready' */
                        public RequisitionPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            // Locators are initialized once
                            this.titleInput = page.locator("#requisitionTitle");
                            this.fundTypeDropdown = page.locator("#fundType");
                            this.submitButton = page.locator("button:has-text('Submit')");
                            this.statusBadge = page.locator("#reqStatus");
                            this.goToFundingLink = page.locator("a:has-text('Funding Lines')");
                    		    this.routeForApprovalButton = page.locator("button:has-text('Route for Approval')");
                    
                            // Explain: constructor wait = stability anchor for “page is ready”
                            pwm.waitVisible("#requisitionTitle");
                        }
                        
                    		// Page-Specific Actions Defined in Page Object Methods:
                        public void createRequisition(String title, String fundType) {
                            /* Explain: business action hides locator detail
                               .type being called from PlaywrightManager class containing Playwright action: locator.fill(value)
                    		        public void type(Locator locator, String value) {
                    			        locator.fill(value);
                    				    }
                               titleInput is a Locator declared as class instance variable and initialized in the Page Object constructor */
                            pwm.type(titleInput, title);
                            
                             /*  fundTypeDropdown is a Locator declared as class instance variable and initialized in the Page Object constructor
                               selectOption() is a Playwright Locator method and takes the fundType String from the parameters when used in the Test Class.
                    		        Why not in PlaywrightManager? - Not every Playwright API needs wrapping. Page Objects can use raw Playwright for niche interactions.
                    						    If you wanted to add a wrapper to PlaywrightManager it would look like this:
                    						    public void selectDropdown(Locator locator, String value) {
                    							    locator.selectOption(value);
                    								}
                    								Then in the page object:
                    									pwm.selectDropdown(fundTypeDropdown, fundType); */
                            fundTypeDropdown.selectOption(fundType);
                            
                            /* .click being called from PlaywrightManager class containing Playwright action: locator.click()
                               public void click(Locator locator) {
                    				     locator.click();
                    			     }
                    			    submitButton is a Locator declared as class instance variable and initialized in the Page Object constructor */
                            pwm.click(submitButton);
                        }
                    		
                        public String getStatus() {
                    		    // statusBadge is a Locator declared as a class instance variable and initialized in the Page Object constructor
                    		    // .textContent() is also a Playwright Locator API method (Locator.textContent() returns the element’s text content - Same concept as Selenium’s getText(), just Playwright’s naming.)
                            return statusBadge.textContent();
                        }
                        
                        **// This Method -> navigates to another page and returns it**
                        // it passes the same page and pwm that was used in this Page Object for end-to-end testing
                    ****    public FundingLinesPage goToFundingLines() {
                            pwm.click(goToFundingLink);
                            return new FundingLinesPage(page, pwm);
                        }
                    
                        **// This Method -> navigates to another page and returns it**
                        // it passes the same page and pwm that was used in this Page Object for end-to-end testing
                    ****    public RoutingApprovalPage routeForApproval() {
                            pwm.click(routeForApprovalButton);
                            return new RoutingApprovalPage(page, pwm);
                        }
                    }
                    }
                    ```
                    
                - **`FundingLinesPage` -> returns** `RoutingApprovalPage`
                    
                    ```java
                    public class FundingLinesPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator addLineButton;
                        private final Locator amountInput;
                        private final Locator saveLineButton;
                        private final Locator continueToRoutingButton;
                    
                        public FundingLinesPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.addLineButton = page.locator("button:has-text('Add Line')");
                            this.amountInput = page.locator("#fundAmount");
                            this.saveLineButton = page.locator("button:has-text('Save')");
                            this.continueToRoutingButton = page.locator("button:has-text('Continue to Routing')");
                    
                            pwm.waitVisible("text=Funding Lines");
                        }
                    
                        public FundingLinesPage addFundingLine(String amount) {
                            pwm.click(addLineButton);
                            pwm.type(amountInput, amount);
                            pwm.click(saveLineButton);
                            return this;
                        }
                    
                    		**// This Method -> navigates to the RoutingApprovalPage and returns it**
                        // it passes the same 'page' and 'pwm' that was used in this Page Object for end-to-end testing
                        public RoutingApprovalPage continueToRouting() {
                            pwm.click(continueToRoutingButton);
                            return new RoutingApprovalPage(page, pwm);
                        }
                    }
                    ```
                    
                - `RoutingApprovalPage` **-> returns** `StatusTrackerPage`
                    
                    ```java
                    public class RoutingApprovalPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator selectApproverDropdown;
                        private final Locator submitRoutingButton;
                    
                        public RoutingApprovalPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.selectApproverDropdown = page.locator("#approver");
                            this.submitRoutingButton = page.locator("button:has-text('Submit Routing')");
                    
                            pwm.waitVisible("text=Routing");
                        }
                    
                    		**// This Method -> navigates to the RoutingApprovalPage and returns it**
                        // it passes the same 'page' and 'pwm' that was used in this Page Object for end-to-end testing
                        public StatusTrackerPage submitForApproval(String approver) {
                            selectApproverDropdown.selectOption(approver);
                            pwm.click(submitRoutingButton);
                            return new StatusTrackerPage(page, pwm);
                        }
                    }
                    ```
                    
                - `StatusTrackerPage` ****(final validation page)
                    
                    ```java
                    public class StatusTrackerPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator statusBadge;
                    
                        public StatusTrackerPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                            this.statusBadge = page.locator("#reqStatus");
                            pwm.waitVisible("#reqStatus");
                        }
                    
                        public String getStatus() {
                            return statusBadge.textContent();
                        }
                    }
                    ```
                    
            - DAWMS Page Objects
                - `DAWMSDashboardPage` **→ goes to** `SubmissionIntakePage`
                    
                    ```java
                    public class DAWMSDashboardPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator submissionIntakeBtn;
                    
                        public DAWMSDashboardPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.submissionIntakeBtn = page.locator("button:has-text('Submission Intake')");
                    
                            pwm.waitVisible("text=DAWMS Dashboard");
                        }
                    
                        public SubmissionIntakePage goToSubmissionIntake() {
                            pwm.click(submissionIntakeBtn);
                            return new SubmissionIntakePage(page, pwm);
                        }
                    }
                    ```
                    
                - `SubmissionIntakePage` **→ returns** `ReviewerAssignmentPage`
                    
                    ```java
                    public class SubmissionIntakePage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator submissionTypeDropdown;
                        private final Locator applicationNumberInput;
                        private final Locator createSubmissionButton;
                    
                        public SubmissionIntakePage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.submissionTypeDropdown = page.locator("#submissionType");
                            this.applicationNumberInput = page.locator("#applicationNumber");
                            this.createSubmissionButton = page.locator("button:has-text('Create Submission')");
                    
                            // Stability anchor
                            pwm.waitVisible("#submissionType");
                        }
                    
                        public ReviewerAssignmentPage createSubmission(String submissionType, String appNumber) {
                            submissionTypeDropdown.selectOption(submissionType);  // Playwright method
                            pwm.type(applicationNumberInput, appNumber);
                            pwm.click(createSubmissionButton);
                    
                            // Navigation to next step in workflow
                            return new ReviewerAssignmentPage(page, pwm);
                        }
                    }
                    ```
                    
                - `ReviewerAssignmentPage` **→ returns** `SignatureRoutingPage`
                    
                    ```java
                    public class ReviewerAssignmentPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator reviewerRoleDropdown;
                        private final Locator reviewerNameInput;
                        private final Locator assignReviewerButton;
                        private final Locator continueToSignatureButton;
                    
                        public ReviewerAssignmentPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.reviewerRoleDropdown = page.locator("#reviewerRole");
                            this.reviewerNameInput = page.locator("#reviewerName");
                            this.assignReviewerButton = page.locator("button:has-text('Assign')");
                            this.continueToSignatureButton = page.locator("button:has-text('Route to Signature')");
                    
                            pwm.waitVisible("text=Reviewer Assignment");
                        }
                    
                        public ReviewerAssignmentPage assignReviewer(String role, String reviewerName) {
                            reviewerRoleDropdown.selectOption(role);
                            pwm.type(reviewerNameInput, reviewerName);
                            pwm.click(assignReviewerButton);
                            return this;
                        }
                    
                        public SignatureRoutingPage routeToSignatureStep() {
                            pwm.click(continueToSignatureButton);
                            return new SignatureRoutingPage(page, pwm);
                        }
                    }
                    
                    ```
                    
                - `SignatureRoutingPage` **→ returns** `MilestoneStatusPage`
                    
                    ```java
                    public class SignatureRoutingPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator signerDropdown;
                        private final Locator routeForSignatureButton;
                    
                        public SignatureRoutingPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.signerDropdown = page.locator("#signer");
                            this.routeForSignatureButton = page.locator("button:has-text('Submit for Signature')");
                    
                            pwm.waitVisible("text=Signature Routing");
                        }
                    
                        public MilestoneStatusPage submitForSignature(String signerRoleOrName) {
                            signerDropdown.selectOption(signerRoleOrName);
                            pwm.click(routeForSignatureButton);
                            return new MilestoneStatusPage(page, pwm);
                        }
                    }
                    
                    ```
                    
                - `MilestoneStatusPage` (final validation page)
                    
                    ```java
                    public class MilestoneStatusPage {
                    
                        private final Page page;
                        private final PlaywrightManager pwm;
                    
                        private final Locator milestoneLabel;
                        private final Locator statusLabel;
                    
                        public MilestoneStatusPage(Page page, PlaywrightManager pwm) {
                            this.page = page;
                            this.pwm = pwm;
                    
                            this.milestoneLabel = page.locator("#milestone");
                            this.statusLabel = page.locator("#status");
                    
                            pwm.waitVisible("#status");
                        }
                    
                        public String getMilestone() {
                            return milestoneLabel.textContent(); // Playwright Locator API
                        }
                    
                        public String getStatus() {
                            return statusLabel.textContent();
                        }
                    }
                    
                    ```
                    
        - **Test classes** initialize ****these **Page Objects** and call their **business-level methods**, which **allows tests to read like real workflows instead of low-level UI interactions.**
            
            <aside>
            🎙️
            
            - For CBAPS
                
                “Each Page method represents a real business action, like creating a requisition, adding funding lines, routing for approval, and validating the status transition. Each step in the test returns the next page object so the test expresses workflow transitions. 
                
                That’s how we model real CBAPS routing flows and validate status changes. When a method returns the next Page Object, the test naturally mirrors the real system progression: it starts on Requisition creation, moves to Funding, then Routing, then Status tracking. That return pattern forces the test to follow the same sequence the business follows, and it makes the test readable to both QA and stakeholders because it matches how CBAPS users actually operate.
                
                The validation isn’t just ‘element exists’ — the key assertion is the workflow result: status changes, milestone updates, and routing outcomes, which are the real business rules in these systems.”
                
            - For DAWMS
                
                “In DAWMS, Page Objects map to major stages of the drug submission workflow — intake, assignment, routing, and milestone/status tracking. Each Page method represents a business action such as creating an intake record, assigning a reviewer role, routing to signature or the next gate, and verifying milestone transitions.
                
                Each time the workflow moves to the next stage, the method returns the next Page Object, so the test follows the same progression DAWMS users follow — Intake → Assign Reviewer → Signature Routing → Milestone/Status verification. That design forces the test to reflect the real operational sequence, and it keeps locators and UI changes isolated inside Page Objects instead of spreading them across tests.
                
                The validations focus on workflow correctness: status and milestone transitions, gating rules, and routing outcomes — because those are the true business rules in DAWMS, not just whether a button appears.
                
                And just like CBAPS, we log each step into ExtentReports so the execution output reads like a traceable workflow and provides strong evidence when a test fails.”
                
            
            Tests extend Base to avoid duplicating setup and teardown code.
            
            Tests are supposed to read like workflows:
            
            - `HomePage.searchCourse()`
            - `ProductTypePage.addToCart()`
            - `CheckoutPage.createAccount()`
            
            In FDA terms:
            
            - `RequisitionPage.createRequisition()`
            - `FundingLinesPage.addFundingLines()`
            - `RoutingPage.submitForApproval()`
            - `StatusPage.verifyWorkflowStatus()`
            - What `test = extent.createTest()` and `addStepToReport()` does in practice
                
                In the Extent HTML report, that test will show a **timeline** like:
                
                - INFO Step 1: Created requisition…
                - INFO Step 2: Added funding line…
                - INFO Step 3: Navigated to routing…
                - INFO Step 4: Submitted routing…
                - PASS/FAIL with screenshot/video if failure happens
                
                **This matters in enterprise projects** because it:
                
                - makes failures explainable fast
                - gives audit-style evidence (“what step did it fail on?”)
                - helps non-QA stakeholders understand test intent
            </aside>
            
            - `CBAPS_EndToEnd_Test` Class
                
                ```java
                // Typical imports include: 
                import static org.assertj.core.api.Assertions.*;
                
                import org.slf4j.Logger;   <--- Logger uses LoggerFactory to make logs
                import org.slf4j.LoggerFactory;
                import org.testng.annotations.Test;
                
                import com.aventstack.extentreports.Status;
                import com.playwright.cbaps.pages.HomePage;
                import com.playwright.cbaps.pages.RequisitionPage;
                import com.playwright.cbaps.pages.ProceedToCheckoutPage;
                import com.playwright.cbaps.pages.ProductTypePage;
                import com.playwright.cbaps.pages.ProductTypes;
                import com.playwright.cbaps.pages.SearchCourseResultPage;
                import com.playwright.week5.library.Base;
                
                public class CBAPS_EndToEnd_Test extends Base {
                	
                	// Declare the Logger (coming from slf4j)
                	private static final Logger log = LoggerFactory.getLogger(BuyACourseTestScript.class);
                
                    @Test
                    public void cbaps_createReq_addFunding_route_verifyStatus() {
                    
                    		/* Think of ExtentReports => "test run journal"
                					 	**extent** = the full report for the whole run (suite-level object)
                					 	**test** = a single test case entry inside that report (one row/card in the HTML report)
                				 	What the line below does: Creates a new test node in the Extent HTML report with that name.
                				 	Everything you log after that (steps, passes, fails, screenshots) attaches to this test node.
                				 	Usually put it in @BeforeMethod automatically (best practice) but you can put it inside the test method.
                				*/
                				test = extent.createTest("CBAPS E2E: Create Req → Funding → Routing → Status");
                		    
                		    // Page 0: Portal
                        // Page object takes Page + wrapper
                        PortalHomePage portal = new PortalHomePage(page, myPlaywright);
                        //Using the helper method below to report steps and also logging them to the console.
                        addStepToReport("Step 1: Opened portal home page.");
                        
                        // Page 1: CBAPS Dashboard
                 	      // test reads like real CBAPS business flow
                        CBAPSDashboardPage dashboard = portal.openCBAPS();
                        addStepToReport("Step 2: Navigated to CBAPS Dashboard.");
                		    
                		    // Page 2: Requisition
                        RequisitionPage reqPage = dashboard.goToCreateRequisition();
                        addStepToReport("Step 3: Opened Create Requisition page.");
                
                        reqPage.createRequisition("FY26 Cloud Tools", "Operations");
                		    addStepToReport("Step 4: Created requisition with title + fund type.");
                        
                        // Page 3: Funding Lines
                        FundingLinesPage fundingPage = reqPage.goToFundingLines()
                        fundingPage.addFundingLine("5000");
                        addStepToReport("Step 5: Added funding line and saved.");
                        
                        // Page 4: Routing
                        RoutingApprovalPage routingPage = fundingPage.continueToRouting();
                        addStepToReport("Step 6: Navigated to routing page.");
                        
                        // Page 5: Status Tracker
                        StatusTrackerPage statusPage = routingPage.submitForApproval("Branch Chief");
                		    addStepToReport("Step 7: Submitted routing for approval.");
                
                        // Assertion validates workflow outcome
                        Assert.assertEquals(statusPage.getStatus(), "Submitted");
                	      addStepToReport("Step 8: Verified workflow status transitioned to Submitted.");
                    }
                    
                    // Helper Method that logs test steps by passing the String testStep in the method each step.
                    // This can go here in the test class or in the @BeforeMethod in the Base Class
                    // Optionally also logs to console (logger.into(...))
                    // Sometimes adds screenshots as well
                    // So instead of sprinkling raw Extent calls everywhere, you centralize logging in one helper.
                    private void addStepToReport(String testStep) {
                				test.log(Status.PASS, testStep);	
                				log.info(testStep);
                	}
                }
                ```
                
            - `DAWMS_EndToEnd_Test` Class
                
                ```java
                public class DAWMS_EndToEnd_Test extends Base {
                
                    @Test
                    public void dawms_intake_assign_routeSignature_verifyMilestone() {
                
                        test = extent.createTest("DAWMS E2E: Intake → Assign Reviewer → Signature → Milestone");
                
                        // Page 0: Portal
                        PortalHomePage portal = new PortalHomePage(page, myPlaywright);
                        addStepToReport("Opened portal home page.");
                
                        // Page 1: DAWMS Dashboard
                        DAWMSDashboardPage dashboard = portal.openDAWMS();
                        addStepToReport("Navigated to DAWMS Dashboard.");
                
                        // Page 2: Submission Intake
                        SubmissionIntakePage intake = dashboard.goToSubmissionIntake();
                        addStepToReport("Opened Submission Intake page.");
                
                        ReviewerAssignmentPage assignment = intake.createSubmission("NDA", "123456");
                        addStepToReport("Created submission intake record.");
                
                        // Page 3: Reviewer Assignment
                        SignatureRoutingPage signature = assignment
                                .assignReviewer("Clinical Reviewer", "Jane Doe")
                                .routeToSignatureStep();
                        addStepToReport("Assigned reviewer and moved to signature routing.");
                
                        // Page 4: Signature → Milestone/Status
                        MilestoneStatusPage status = signature.submitForSignature("Division Director");
                        addStepToReport("Submitted workflow to signature routing.");
                
                        Assert.assertEquals(status.getStatus(), "Pending Signature");
                        addStepToReport("Verified status transitioned to Pending Signature.");
                
                        Assert.assertEquals(status.getMilestone(), "Signature Routing");
                        addStepToReport("Verified milestone updated to Signature Routing.");
                    }
                }
                ```
                
        - **To avoid duplicating raw Playwright calls**, a **`PlaywrightManager`** acts as a wrapper around Playwright and owns the **Playwright**, **Browser**, **BrowserContext**, and **Page objects**. This manager exposes common actions such as clicking elements, entering text, waiting for visibility, taking screenshots, and handling file uploads, which **Page Objects** reuse **for consistent and stable interactions.**
            
            <aside>
            🎙️
            
            “This wrapper centralizes browser/context creation + common actions so Page Objects don’t duplicate low-level code.”
            
            - `PlaywrightManager` is a helper/wrapper around Playwright primitives like:
                - `page.locator()`  → you then pass the locator String as a parameter when used in Page Object
                - `click()`
                - `fill()`
                - waits, screenshots, dropdown select, file upload, etc.
            
            So instead of repeating raw Playwright calls everywhere, your Page Objects call:
            
            - `myPlaywrightManager.clickElement(locator)` or
                - `pwm.clickElement(locator)`
            - `myPlaywrightManager.enterText(locator, value)` or
                - `pwm.enterText(locator, value)`
            - `myPlaywrightManager.waitUntilElementVisible(selector)` or
                - `pwm.waitUntilElementVisible(selector)`
            </aside>
            
            ```java
            public class PlaywrightManager {
            
                private Playwright playwright;
                private Browser browser;
                private BrowserContext context;
                private Page page;
            
                public void initPlaywright(String browserType, boolean headless, boolean recordVideo) {
                    playwright = Playwright.create();
            
                    BrowserType.LaunchOptions options = new BrowserType.LaunchOptions()
                            .setHeadless(headless);
            
                    // Explain: choosing browser at runtime (chrome/firefox/webkit)
                    if ("chrome".equalsIgnoreCase(browserType)) {
                        browser = playwright.chromium().launch(options);
                    } else if ("firefox".equalsIgnoreCase(browserType)) {
                        browser = playwright.firefox().launch(options);
                    } else {
                        browser = playwright.webkit().launch(options);
                    }
            
                    Browser.NewContextOptions ctxOptions = new Browser.NewContextOptions()
                            .setIgnoreHTTPSErrors(true);
            
                    // Explain: recordVideo is optional, but useful for CI evidence
                    if (recordVideo) {
                        ctxOptions.setRecordVideoDir(Paths.get("target/videos"));
                    }
            
                    context = browser.newContext(ctxOptions);
                }
            
                public Page openNewBrowserPage() {
                    page = context.newPage();
                    return page;
                }
            
                // ---- wrapped helpers used by Page Objects ----
            
                public void click(Locator locator) {
                    locator.click();
                }
            
                public void type(Locator locator, String value) {
                    locator.fill(value);
                }
            
                public void waitVisible(String selector) {
                    page.waitForSelector(selector);
                }
            
                public String takeBase64Screenshot() {
                    byte[] bytes = page.screenshot(new Page.ScreenshotOptions().setFullPage(true));
                    return Base64.getEncoder().encodeToString(bytes);
                }
            
                public void closePage() {
                    if (page != null) page.close();
                }
            
                public void closeAll() {
                    if (context != null) context.close();
                    if (browser != null) browser.close();
                    if (playwright != null) playwright.close();
                }
            }
            
            ```
            
        - **Test classes** inherit from a `Base` class, which controls the test lifecycle using **TestNG annotations**. The **Base class** is responsible for initializing the `PlaywrightManager`, creating a fresh **Page** before each test method, and handling teardown logic such as closing pages, capturing screenshots, recording videos, and reporting failures.
        Importantly, the **Base class** does not inherit from Playwright. Instead, it **owns an instance** of `PlaywrightManager`, which internally manages Playwright resources.
            
            <aside>
            🎙️
            
            “**TestNG** **annotations** drive **setup/teardown**. 
            **Base** doesn’t extend Playwright. Base **owns** `PlaywrightManager` (because it is responsible for creation and teardown of Playwright resources) while `PlaywrightManager` manages Playwright resources. `Tests` only consume it.”
            
            - Base has a **field reference** (Class Instance Variable) to `PlaywrightManager` **(owns it)**
            - Base is responsible for **creating it** and **controlling its lifecycle** (maintaining and closing it) **(owns it)**
            - **Tests don’t create the PlaywrightManager** — **they inherit Base and reuse it**
            
            `Base` is your test harness:
            
            - **Initializes ExtentReports** **once per suite**
                
                ```java
                    @BeforeSuite
                    public void beforeSuite() {
                        // Explain: suite-level reporting init (one report for the whole run)
                        extent = ExtentReportManager.getInstance();
                    }
                ```
                
            - **Initializes Playwright** **once per class**
                
                ```java
                	@BeforeClass
                		public void setup() {
                		    pwm = new PlaywrightManager(); // Base creates/owns it
                		    pwm.initPlaywright(...);
                		}
                ```
                
            - **Creates a fresh Page** **per test method**
                
                ```java
                    @BeforeMethod
                    public void beforeMethod(Method method) {
                        page = pwm.openNewBrowserPage();
                    }
                ```
                
            - **Handles teardown** + **screenshot/report/video** **on failures**
                
                ```java
                    @AfterMethod
                    public void afterMethod(ITestResult result) {
                        if (!result.isSuccess()) {
                            String base64 = pwm.takeBase64Screenshot();
                            test.fail(result.getThrowable());
                            test.addScreenCaptureFromBase64String(base64, "Failure Screenshot");
                        }
                        pwm.closePage();
                    }
                ```
                
            
            So tests extend Base to avoid duplicating setup code.
            
            **Base *has a*** `PlaywrightManager`, and the `PlaywrightManager` **has** **Playwright** + **Browser** + **Context** + **Page**.
            
            So:
            
            - **Base** **extends nothing special** (it just *is* a TestNG base class)
            - **Base** uses a field like: `protected PlaywrightManager myPlaywrightManager;`
            - `PlaywrightManager` internally holds:
                - `Playwright playwright`
                - `Browser browser`
                - `BrowserContext context`
                - `Page page`
            </aside>
            
            ```java
            // Typical Imports Include:
            import org.slf4j.Logger;
            import org.slf4j.LoggerFactory;
            import org.testng.ITestResult;
            import org.testng.annotations.AfterClass;
            import org.testng.annotations.AfterMethod;
            import org.testng.annotations.AfterSuite;
            import org.testng.annotations.BeforeClass;
            import org.testng.annotations.BeforeMethod;
            import org.testng.annotations.BeforeSuite;
            
            import com.aventstack.extentreports.ExtentReports;   <--- report container for the entire run (suite)
            import com.aventstack.extentreports.ExtentTest;      <--- single test case entry inside the report
            import com.aventstack.extentreports.MediaEntityBuilder;
            import com.aventstack.extentreports.Status;
            import com.aventstack.extentreports.model.Media;
            import com.microsoft.playwright.Page;
            
            public class Base {
            
                protected PlaywrightManager pwm;   // wrapper (owns Playwright/Browser/Context/Page)
                protected Page page;               // current test's Page
                
                //Why these matter: If you don’t create a new ExtentTest per test method, all logs can get mixed together.
                // You create it once (usually @BeforeSuite)
                protected ExtentReports extent;    // Think: "the HTML report file builder." extent = whole report
                // You create one ExtentTest per @Test method using extent.createTest(...)
                protected ExtentTest test;         // Think: "one test's timeline/log." test = one test inside the report
            		
            		
                @BeforeSuite
                public void beforeSuite() {
                    // Explain: suite-level reporting init (one report for the whole run)
                    extent = ExtentReportManager.getInstance();
                }
                
                //You can add this method here or in the Test Class. I did it in both to show that you can in both.
                protected void addStepToReport(String msg) {
                    // Shows up in the Extent HTML timeline
                    test.info(msg);
                    // Optional: also log to file/console
                    log.info(msg);
                }
            
                @BeforeClass
                public void beforeClass() {
                    // Explain: create Playwright + Browser + Context ONCE per class for speed
                    pwm = new PlaywrightManager();
                    pwm.initPlaywright("chrome", false /* headless */, true /* video */);
                }
            
                @BeforeMethod
                public void beforeMethod(Method method) {
                    // Explain: new Page per test method = isolation + fewer flaky side effects
                    page = pwm.openNewBrowserPage();
            
                    // You can add it here (best practice) per-test node in the report or inside the Test Method.
                    test = extent.createTest(method.getName());
                }
            
                @AfterMethod
                public void afterMethod(ITestResult result) {
                    // Explain: on failure, capture evidence (screenshot/video) and attach to report
                    if (!result.isSuccess()) {
                        String base64 = pwm.takeBase64Screenshot();
                        test.fail(result.getThrowable());
                        test.addScreenCaptureFromBase64String(base64, "Failure Screenshot");
                    }
            
                    // Explain: close only the Page after each test (context stays for class)
                    pwm.closePage();
                }
            
                @AfterClass
                public void afterClass() {
                    // Explain: clean shutdown at class end
                    pwm.closeAll();
                }
            
                @AfterSuite
                public void afterSuite() {
                    // Explain: flush report output once at the end
                    extent.flush();
                }
            }
            ```
            
        - **This composition-based design keeps responsibilities separated**:
            - **Base** manages **lifecycle** and **orchestration**
            - **PlaywrightManager** manages **browser interactions**, and
            - **Page Objects** encapsulate **UI structure** and **business behavior**.
        
        ---
        
        - For **parallel execution**, I’d ensure each **thread** has its own **BrowserContext** and **Page**, often with **ThreadLocal storage**, **so tests don’t share state.**
            - Need Code Built For this