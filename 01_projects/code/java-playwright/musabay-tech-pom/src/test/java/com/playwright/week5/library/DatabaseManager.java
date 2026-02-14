package com.playwright.week5.library;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DatabaseManager {
	protected static final Logger log = LoggerFactory.getLogger(DatabaseManager.class);

	// Oracle Database Only Replace XE with your SID or use SERVICE format
	//private static final String URL = "jdbc:oracle:thin:@localhost:1521:XE"; 
	private static final String USER_NAME = "hr";
	
	private static final String URL = "jdbc:postgresql://localhost:5432/HRDB2";	
	//private static final String USER_NAME = "postgres";
	private static final String USER_PASSWORD = "hr";

	private Connection connection;

	// constructor
	public DatabaseManager() {
		try {
			connection = DriverManager.getConnection(URL, USER_NAME, USER_PASSWORD);
			log.info("Connected to PostgreSQL database sucessfully.");
		} catch (Exception e) {
			log.error("Connection failed: " + e.getMessage());
		}
	}

	// Read - Select (dynamic columns)
	public String runSelectSingleDataQuery(String inputQuery) {
		String data = null;

		try {
			Statement stmt = connection.createStatement();
			ResultSet rs = stmt.executeQuery(inputQuery);

			// Print each row
			while (rs.next()) {
				data = rs.getString(1);
				log.debug(rs.getString(1) + "\t");
			}
			log.debug("");

		} catch (Exception e) {
			log.error("Executing select query method failed: " + e.getMessage());
		}

		return data;
	}

	// Read - Select (dynamic columns)
	public ResultSet runSelectQuery(String inputQuery) {
		ResultSet rs = null;

		try {
			Statement stmt = connection.createStatement();
			rs = stmt.executeQuery(inputQuery);
			ResultSetMetaData rsmd = rs.getMetaData();
			int columnCount = rsmd.getColumnCount();

			// Print column names
			for (int i = 1; i <= columnCount; i++) {
				log.debug(rsmd.getColumnLabel(i) + "\t");
			}
			log.debug(inputQuery);

			// Print each row
			while (rs.next()) {
				for (int i = 1; i <= columnCount; i++) {
					System.out.print(rs.getString(i) + "\t");
				}
				System.out.println();
			}

		} catch (Exception e) {
			log.error("Executing select query method failed: " + e.getMessage());
		}

		return rs;
	}
	
	
	public static Object[][] resultSetTo2DArray(ResultSet rs) throws SQLException {
	    ResultSetMetaData metaData = rs.getMetaData();
	    int columnCount = metaData.getColumnCount();

	    // Move to the last row to get total row count
	    rs.last();
	    int rowCount = rs.getRow();
	    rs.beforeFirst(); // Reset back to before the first row

	    Object[][] data = new Object[rowCount][columnCount];

	    int rowIndex = 0;
	    while (rs.next()) {
	        for (int colIndex = 0; colIndex < columnCount; colIndex++) {
	            data[rowIndex][colIndex] = rs.getObject(colIndex + 1); // JDBC is 1-based
	        }
	        rowIndex++;
	    }

	    return data;
	}
	
	/*
	@DataProvider(name = "dbDataProvider")
	public Object[][] provideDataFromDB() throws SQLException {
	    DatabaseManager db = new DatabaseManager();
	    ResultSet rs = db.runSelectQuery("SELECT first_name, last_name FROM Employees");
	    return resultSetTo2DArray(rs);
	}
	*/
	
	

	// Testing Database Manager class code / methods
	public static void main(String[] args) throws SQLException {
		DatabaseManager dbManager = new DatabaseManager();
		// dbManager.runSelectQuery("Select employee_id, first_name, last_name, email
		// from Employees;");

		/*
		 * ResultSet data = dbManager.
		 * runSelectQuery("Select first_name from Employees where first_name = 'Amit';"
		 * ); while(data.next()) { String firstName = data.getString(0);
		 * System.out.println("first name: " + firstName); }
		 */

		String query = "Select first_name from Employees where first_name = 'Amit';";
		String myData = dbManager.runSelectSingleDataQuery(query);
		System.out.println("my single data: " + myData);
	}
}