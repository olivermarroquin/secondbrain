package com.playwright.week5.tests;

import org.testng.annotations.Test;
import static org.assertj.core.api.Assertions.*;

import java.sql.Timestamp;

import com.microsoft.playwright.FrameLocator;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.options.AriaRole;
import com.microsoft.playwright.options.LoadState;
import com.microsoft.playwright.options.WaitForSelectorState;
import com.playwright.week5.library.Base;

public class PurchaseAutomation extends Base {

	@Test(enabled = true)
	public void visitURL() {

		try {
			String siteURL = "https://www.thegreatcourses.com/";

			// navigate to site
			page.navigate(siteURL);
			page.waitForLoadState(LoadState.LOAD);
			page.waitForTimeout(1000);
			System.out.println("Step 1: Navigating to website " + page.title());

			// getting website title
			String actualTitle = page.title().trim();
			String expectedTitle = "The Great Courses";
			System.out.println("Page Title: " + actualTitle);

			// asserting website title
			assertThat(actualTitle).as("Step 2: Page title verification failed").isEqualTo(expectedTitle);
			System.out.println("Step 2: Page title verification successful");

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("visitURL method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void searchItem() {
		try {
			visitURL();

			// search field element locator
			Locator searchField = page.locator("#search-field");

			// highlight search field
			myPlaywright.blinkHighlight(page, searchField);

			// searching item
			System.out.println("Step 3: Searching for 'Our Night Sky'");
			searchField.fill("Our Night Sky");

			// search button element locator
			Locator enterButton = page.locator(
					"#root > header > nav > div > div.SearchField.SearchField_isTopTabs_undefined > div > span.SearchField-Icon");

			// highlight search button
			myPlaywright.blinkHighlight(page, enterButton);

			// click search button
			System.out.println("Step 4: Pressing enter");
			enterButton.click();

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("searchItem method failed").isTrue();

		}
	}

	@Test(enabled = true)
	public void selectItem() {
		try {
			searchItem();

			// selected item element locator
			Locator selectedItem = page.locator(
					"#root > main > div > div.SearchPage-Results.flex-fill > div.grid.row > div:nth-child(1) > div > div > a > div > div.card-body > p");

			// wait for item to be visible
			selectedItem.waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE));

			// highlight item to be selected
			myPlaywright.blinkHighlight(page, selectedItem);
			System.out.println("Step 5: Selecting 'Our Night Sky'");

			// click and select item
			selectedItem.click();

			// DVD radio button element locator
			Locator dvdRadioButton = page.locator(
					"#root > main > div:nth-child(4) > section > div.BuyOptions.BuyOptions_isListTile_undefined.BuyOptions_isOwnCourse.BuyOptions_additionalButtonsPlacement_button > div.BuyOptions-OptionsContainer > div:nth-child(2) > div > label");

			// wait for DVD option to be visible
			dvdRadioButton.waitFor(new Locator.WaitForOptions().setState(WaitForSelectorState.VISIBLE));

			// highlight DVD option
			myPlaywright.blinkHighlight(page, dvdRadioButton);

			// select the DVD option
			System.out.println("Step 6: Clicking 'DVD' option");
			dvdRadioButton.click();

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("selectItem method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void addToCartAndCheckout() {

		try {
			selectItem();

			// add to cart button element locator
			Locator addToCartButton = page.locator(
					"#root > main > div:nth-child(4) > section > div.BuyOptions.BuyOptions_isListTile_undefined.BuyOptions_isOwnCourse.BuyOptions_additionalButtonsPlacement_button > div.BuyOptions-BtnWrapper > button");
			
			// wait for add to cart button 
			addToCartButton.waitFor();
			
			// highlight add to cart button
			myPlaywright.blinkHighlight(page, addToCartButton);

			// click add to cart button
			System.out.println("Step 7: Adding to cart");
			addToCartButton.click();

			// check out button element locator
			Locator checkoutButton = page.locator(
					"#root > main > div.UpsellPage-Header > div > div.UpsellPage-Cart > div.UpsellPage-CartButtons > a.ml-2.btn.btn-fill-success");
			
			// wait for checkout button 
			checkoutButton.waitFor();
			
			// highlight checkout button
			myPlaywright.blinkHighlight(page, checkoutButton);

			// click checkout button
			System.out.println("Step 8: Clicking 'Checkout' button ");
			checkoutButton.click();

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("addToCartAndCheckout method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void createAccount() {

		try {
			addToCartAndCheckout();

			// create account button element locator
			Locator createAccountButton = page.locator(
					"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(1) > div > div > div > form > div > div.row > div.newCustomer.text-right.col > button");

			boolean isCreateAccountButtonVisible = createAccountButton.isVisible();

			if (isCreateAccountButtonVisible) {

				// highlight create account button element
				myPlaywright.blinkHighlight(page, createAccountButton);

				// click create account button
				System.out.println("Step 9: Clicking on 'Create Account' button");
				createAccountButton.click();

				// input field visibility check
				Locator emailAddressField = page.locator("#email");
				Locator passwordField = page.locator("#password");

				// wait for input field elements to load
				emailAddressField.waitFor();
				passwordField.waitFor();

				// set boolean for input fields visibility
				boolean isEmailAddressVisible = emailAddressField.isVisible();
				boolean isPasswordFieldVisible = passwordField.isVisible();

				// input the values if all fields are visible
				if (isPasswordFieldVisible && isEmailAddressVisible) {
					System.out.println("Email and password fields are visible");

					if (isPasswordFieldVisible) {
						System.out.println("Step 10: Entering email");

						// highlight email filed element
						myPlaywright.blinkHighlight(page, emailAddressField);

						
						
						// input email address
						emailAddressField.fill(generateNewEmail());
					}

					if (isEmailAddressVisible) {
						System.out.println("Step 11: Entering Password");

						// highlight password filed element
						myPlaywright.blinkHighlight(page, passwordField);

						// input password
						passwordField.fill("Test1234@");
					}
				}
			} else {
				System.out.println("Step 9, 10 and 11 aready compleate");
			}
		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("createAccount method failed").isTrue();
		}
	}

	public String generateNewEmail() {
		String emailBase = "@erapk.com";
		String emailUser = "doyaba460";
		
		java.time.Instant instant = java.time.Instant.now();
	     long timestampMillis = instant.toEpochMilli();
		String dynamicEmail = emailUser + timestampMillis + emailBase;
		System.out.println("new email: " + dynamicEmail);
		return dynamicEmail;
		
	}
	
	
	@Test(enabled = true)
	public void termsCheckBox() {
		try {

			createAccount();
			// terms & condition element locator
			Locator termsAndConditionCheckBox = page.locator("#accept-terms");

			boolean isTermsCheckBoxVisible = termsAndConditionCheckBox.isVisible();

			if (isTermsCheckBoxVisible) {
				// check the terms & condition box if not already checked
				boolean checkStatus = termsAndConditionCheckBox.isChecked();

				if (!checkStatus) {
					System.out.println("Step 12: Checking terms and condition box");

					// terms & condition check box locator
					Locator checkBox = page.locator(
							"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(1) > div > div > div > form > div > div.TermsAndConditions.undefined.form-group > div");

					// highlight terms & condition field
					myPlaywright.blinkHighlight(page, checkBox);

					// terms & condition box check action
					termsAndConditionCheckBox.dispatchEvent("click");
				}

				// continue button element locator
				Locator continueButton = page.locator(
						"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(1) > div > div > div > form > div > button.mt-4.btn.btn-dark.btn-block");

				// wait for continue button 
				continueButton.waitFor();
				
				// highlight continue button element
				myPlaywright.blinkHighlight(page, continueButton);

				// click continue button
				System.out.println("Step 13: Clicking 'Continue' button");
				continueButton.click();
			} else {
				System.out.println("Step 12 & 13 already done");
			}

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("checkBox method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void fillBillingAddress() {

		try {
			termsCheckBox();

			// locate shipping card info field
			Locator shippingInfoCard = page.locator(
					"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(3) > button");
			
			// set boolean status for shipping card field
			boolean isShippingInfoCardVisible = shippingInfoCard.isVisible();

			// if shipping card info field is not visible then continue with inputing billing address info 
			if (!isShippingInfoCardVisible) {

				page.waitForLoadState(LoadState.LOAD);

				// locate address card
				Locator billingAddressCard = page.locator(
						"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(2) > div");

				// set boolean visible status for address card
				boolean isAddressPageLoaded = billingAddressCard.isVisible();

				// if billing address field is visible then input values in those fields
				if (isAddressPageLoaded) {

					// locate address card input elements
					Locator firstName = page.getByRole(AriaRole.TEXTBOX,
							new Page.GetByRoleOptions().setName("First Name First Name"));
					Locator lastName = page.getByRole(AriaRole.TEXTBOX,
							new Page.GetByRoleOptions().setName("Last Name Last Name"));
					Locator streetAddress = page.getByRole(AriaRole.TEXTBOX,
							new Page.GetByRoleOptions().setName("Street Address Street Address"));
					Locator streetAddress2 = page.getByRole(AriaRole.TEXTBOX,
							new Page.GetByRoleOptions().setName("Street Address 2 Street Address"));
					Locator city = page.getByRole(AriaRole.TEXTBOX, new Page.GetByRoleOptions().setName("City City"));
					Locator state = page.getByLabel("State/Province");
					Locator postalCode = page.getByRole(AriaRole.TEXTBOX,
							new Page.GetByRoleOptions().setName("Zip/Postal Code Zip/Postal"));
					Locator country = page.getByLabel("Country");
					Locator phoneNumber = page.getByRole(AriaRole.TEXTBOX,
							new Page.GetByRoleOptions().setName("Phone Number (Optional) Phone"));

					// wait for address card input elements to load
					firstName.waitFor();
					lastName.waitFor();
					streetAddress.waitFor();
					streetAddress2.waitFor();
					city.waitFor();
					state.waitFor();
					postalCode.waitFor();
					country.waitFor();
					phoneNumber.waitFor();

					// set address card input element visible status to boolean
					boolean isFirstNameVisible = firstName.isVisible();
					boolean isLastNameVisible = lastName.isVisible();
					boolean isStreetAddressVisible = streetAddress.isVisible();
					boolean isStreetAddress2Visible = streetAddress2.isVisible();
					boolean isCityVisible = city.isVisible();
					boolean isStateVisible = state.isVisible();
					boolean isPostalCodeVisible = postalCode.isVisible();
					boolean isCountryVisible = country.isVisible();
					boolean isPhoneNumberVisible = phoneNumber.isVisible();

					// if all fields are visible continue with inputting value
					if (isFirstNameVisible && isLastNameVisible && isStreetAddressVisible && isStreetAddress2Visible
							&& isCityVisible && isStateVisible && isPostalCodeVisible && isCountryVisible
							&& isPhoneNumberVisible) {
						System.out.println("All billing address input fields are visible");
						System.out.println("Step 14: Completing billing Address section");

						if (isFirstNameVisible) {
							// highlight first name field
							myPlaywright.blinkHighlight(page, firstName);

							// input first name
							System.out.println("-Entering 'First Name'");
							firstName.fill("Dave");
						}

						if (isLastNameVisible) {
							// highLight last name field
							myPlaywright.blinkHighlight(page, lastName);
							System.out.println("-Entering 'Last Name'");

							// input last name
							lastName.fill("Franco");
						}
						
						if (isStreetAddressVisible) {
							// highlight street address field
							myPlaywright.blinkHighlight(page, streetAddress);
							System.out.println("-Entering 'Street Address'");

							// input street address value
							streetAddress.fill("123 Main Circle");
						}

						if (isCityVisible) {
							// highlight city field
							myPlaywright.blinkHighlight(page, city);
							System.out.println("-Entering 'City'");

							// input city value
							city.fill("Chantilly");
						}

						if (isStateVisible) {
							// highlight state field
							myPlaywright.blinkHighlight(page, state);
							System.out.println("-Selecting 'State'");

							// select state option
							state.selectOption("61");
						}

						if (isPostalCodeVisible) {
							// highlight postal code field
							myPlaywright.blinkHighlight(page, postalCode);
							System.out.println("-Entering 'Postal Code'");

							// input postal code value
							postalCode.fill("22151");
						}

						if (isCountryVisible) {
							// highlight country field
							myPlaywright.blinkHighlight(page, country);
							System.out.println("-Selecting 'Country'");

							// select country option
							country.selectOption("US");
						}

						if (isPhoneNumberVisible) {
							// highlight phone number
							myPlaywright.blinkHighlight(page, phoneNumber);
							System.out.println("-Entering 'Phone Number'");

							// input phone number value
							phoneNumber.fill("7031231234");
						}
					}
					// locate add new address button
					Locator addTheNewAddressButton = page.locator(
							"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(2) > div > div > div > form > button");

					// highlight add new address button
					myPlaywright.blinkHighlight(page, addTheNewAddressButton);

					// click add new address button button
					System.out.println("Step 15: Clicking 'Add the new address' button");
					addTheNewAddressButton.click();
				} else {
					System.out.println("Step 14 & 15 done as profile already exixsts");
				}
			} else {
				System.out.println("Step 14 & 15 done as profile already exixsts");
			}

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("fillBillingAddress method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void shippingOptions() {
		try {
			fillBillingAddress();

			// locate ship to billing address check box
			Locator shipToBillingCheckbox = page.locator("#ship-to-billing");
			
			// wait for ship to billing address check box
			shipToBillingCheckbox.waitFor();
			myPlaywright.sleep(2);
			// set boolean status for locate ship to billing address check box checked
			boolean checkBoxStatus = shipToBillingCheckbox.isChecked();

			// check the box if it is not checked already
			if (!checkBoxStatus) {

				// ship to billing address check box locator
				Locator checkBox = page.locator(
						"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(2) > div > div > div > div.my-3.form-check > label");

				// highlight ship to billing address check box
				myPlaywright.blinkHighlight(page, checkBox);

				// ship to billing address check box click action
				System.out.println("Step 16: Clicking 'Ship to Billing Address'");
				shipToBillingCheckbox.dispatchEvent("click");
			}
			// continue button locator
			Locator continueButton = page.locator(
					"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(2) > div > div > div > button.btn.btn-dark.btn-block");

			// wait for continue button 
			continueButton.waitFor();
			
			// highlight continue button
			myPlaywright.blinkHighlight(page, continueButton);

			// continue button click action
			System.out.println("Step 17: Clicking 'Continue' button");
			continueButton.click();

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("shippingOptions method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void shippingSpeed() {

		try {
			shippingOptions();

			// locate 2nd day radio button
			Locator secondDayRadioButton = page.locator(
					"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(3) > div > div > div > div.ShippingMethods > div > div:nth-child(2) > label");

			//wait for second day radio button
			secondDayRadioButton.waitFor();
			
			// highlight 2nd day radio button
			myPlaywright.blinkHighlight(page, secondDayRadioButton);

			// click on second day option
			System.out.println("Step 18: Selecting '2nd day' option");
			secondDayRadioButton.click();

			// locate continue button
			Locator continueButton = page.locator(
					"#root > main > section > div > div > div > div.col-lg-15.col-md-16 > div > div > div:nth-child(3) > div > div > div > button.btn.btn-dark.btn-block");

			// highlight continue button
			myPlaywright.blinkHighlight(page, continueButton);

			// click continue button
			System.out.println("Step 19: Clicking 'Continue' button");
			continueButton.click();

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("shippingSpeed method failed").isTrue();
		}
	}

	@Test(enabled = true)
	public void paymentInfo() {
		try {

			shippingSpeed();

			// payment info element Locator
			Locator cardNumberFiled = page.locator("iframe[name=\"access-worldpay-pan\"]").contentFrame()
					.getByRole(AriaRole.TEXTBOX, new FrameLocator.GetByRoleOptions().setName("Card number"));
			Locator expDate = page.locator("iframe[name=\"access-worldpay-expiry\"]").contentFrame()
					.getByRole(AriaRole.TEXTBOX, new FrameLocator.GetByRoleOptions().setName("Expiry date"));
			Locator ccvCode = page.locator("iframe[name=\"access-worldpay-cvv\"]").contentFrame()
					.getByRole(AriaRole.TEXTBOX, new FrameLocator.GetByRoleOptions().setName("Security code"));

			// wait for payment info element to load
			cardNumberFiled.waitFor();
			expDate.waitFor();
			ccvCode.waitFor();

			// set visible status for payment info field
			boolean isCardNumberFiledVisible = cardNumberFiled.isVisible();
			boolean isExpDateVisible = expDate.isVisible();
			boolean isCcvCodeVisible = ccvCode.isVisible();

			// if conditions to fill up card info if fields are visible
			if (isCardNumberFiledVisible && isExpDateVisible && isCcvCodeVisible) {
				System.out.println("Step 20: Entering payment info as all payment fields are visible");

				if (isCardNumberFiledVisible) {
					// highlight card number field
					myPlaywright.blinkHighlight(page, cardNumberFiled);
					// input card number value
					cardNumberFiled.fill("5127880999999990");
				}

				if (isExpDateVisible) {
					// highlight expiration date field
					myPlaywright.blinkHighlight(page, expDate);
					// input expiration date value
					expDate.fill("0330");
				}

				if (isCcvCodeVisible) {
					// highlight security code field
					myPlaywright.blinkHighlight(page, ccvCode);
					// input security code value
					ccvCode.fill("737");
				}
			}

		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("paymentInfo method failed").isTrue();
		}
	}

	@Test
	public void runThreeTimes() {
		try {
			for (int i = 1; i <= 3; i++) {
				paymentInfo();
			}
		} catch (Exception e) {
			e.printStackTrace();
			assertThat(false).as("runThreeTimes method failed").isTrue();
		}
	}
	
}
