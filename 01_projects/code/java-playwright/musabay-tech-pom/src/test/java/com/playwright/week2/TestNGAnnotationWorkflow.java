package com.playwright.week2;

import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class TestNGAnnotationWorkflow {
	
	@BeforeClass
	public void beforeTestClass() {
		System.out.println("this will run only one time before-All-Tests start.");
	}
	
	@AfterClass
	public void afterTestClass() {
		System.out.println("this will run only one time after-All-Tests completed.");
	}
	
	@BeforeMethod
	public void setUp() {
		System.out.println("this is setUp method which will run before evey single test start.");
	}
	
	@AfterMethod
	public void tearDown() {
		System.out.println("this is tearDown method which will run after evey single test complete.");
	}
	
	@Test
	public void myTest1() {
		System.out.println("This is myTest1 test.");
	}
	
	@Test
	public void myTest2() {
		System.out.println("This is myTest2 test.");
	}
	
	
}









