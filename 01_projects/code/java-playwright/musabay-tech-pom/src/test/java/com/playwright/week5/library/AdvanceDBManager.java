package com.playwright.week5.library;


import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Generic database utility for Playwright UI test verification.
 * Supports PostgreSQL, MySQL, Microsoft SQL Server, and Oracle connections.
 *
 * <h2>JDBC Driver Dependencies (pom.xml)</h2>
 * This class requires the corresponding JDBC driver in pom.xml for the database you are connecting to.
 * If your database server is upgraded to a newer version, update the driver version in pom.xml accordingly.
 *
 * <pre>
 * | Database     | GroupId                        | ArtifactId         | Current Version   | Default Port |
 * |--------------|--------------------------------|--------------------|-------------------|--------------|
 * | PostgreSQL   | org.postgresql                 | postgresql         | 42.7.3            | 5432         |
 * | MySQL        | com.mysql                      | mysql-connector-j  | 9.1.0             | 3306         |
 * | SQL Server   | com.microsoft.sqlserver        | mssql-jdbc         | 12.8.1.jre11      | 1433         |
 * | Oracle       | com.oracle.database.jdbc       | ojdbc11            | 23.5.0.24.07      | 1521         |
 * </pre>
 *
 * <b>NOTE:</b> Always keep driver versions compatible with your database server version.
 * Check Maven Central for the latest versions:
 * - PostgreSQL:  https://mvnrepository.com/artifact/org.postgresql/postgresql
 * - MySQL:       https://mvnrepository.com/artifact/com.mysql/mysql-connector-j
 * - SQL Server:  https://mvnrepository.com/artifact/com.microsoft.sqlserver/mssql-jdbc
 * - Oracle:      https://mvnrepository.com/artifact/com.oracle.database.jdbc/ojdbc11
 *
 * <h2>Usage Examples</h2>
 * <pre>
 * // PostgreSQL
 * AdvanceDBManager db = AdvanceDBManager.postgresql("localhost", 5432, "mydb", "user", "pass");
 *
 * // MySQL
 * AdvanceDBManager db = AdvanceDBManager.mysql("localhost", 3306, "mydb", "user", "pass");
 *
 * // SQL Server
 * AdvanceDBManager db = AdvanceDBManager.sqlServer("localhost", 1433, "mydb", "user", "pass");
 *
 * // Oracle (SID)
 * AdvanceDBManager db = AdvanceDBManager.oracle("localhost", 1521, "ORCL", "user", "pass");
 *
 * // Oracle (Service Name)
 * AdvanceDBManager db = AdvanceDBManager.oracleService("localhost", 1521, "myservice", "user", "pass");
 *
 * // Custom JDBC URL
 * AdvanceDBManager db = new AdvanceDBManager("jdbc:postgresql://localhost:5432/mydb", "user", "pass");
 *
 * // Then execute queries:
 * List&lt;Map&lt;String, Object&gt;&gt; rows = db.executeQuery("SELECT * FROM users WHERE email = ?", "alice@example.com");
 * assertEquals("Alice", rows.get(0).get("name"));
 * db.close();
 * </pre>
 */
public class AdvanceDBManager {

	private Connection connection;
	private String dbType;

	/**
	 * Creates a AdvanceDBManager with a custom JDBC URL.
	 * Auto-detects database type from the URL.
	 */
	public AdvanceDBManager(String url, String user, String password) {
		try {
			this.dbType = detectDbType(url);
			connection = DriverManager.getConnection(url, user, password);
			System.out.println("Connected to " + dbType + " database successfully.");
		} catch (SQLException e) {
			throw new RuntimeException("Database connection failed: " + e.getMessage(), e);
		}
	}

	/**
	 * Factory method for PostgreSQL connections.
	 *
	 * Example:
	 *   AdvanceDBManager db = AdvanceDBManager.postgresql("localhost", 5432, "mydb", "user", "pass");
	 */
	public static AdvanceDBManager postgresql(String host, int port, String database, String user, String password) {
		String url = "jdbc:postgresql://" + host + ":" + port + "/" + database;
		return new AdvanceDBManager(url, user, password);
	}

	/**
	 * Factory method for MySQL connections.
	 *
	 * Example:
	 *   AdvanceDBManager db = AdvanceDBManager.mysql("localhost", 3306, "mydb", "user", "pass");
	 */
	public static AdvanceDBManager mysql(String host, int port, String database, String user, String password) {
		String url = "jdbc:mysql://" + host + ":" + port + "/" + database;
		return new AdvanceDBManager(url, user, password);
	}

	/**
	 * Factory method for SQL Server connections.
	 *
	 * Example:
	 *   AdvanceDBManager db = AdvanceDBManager.sqlServer("localhost", 1433, "mydb", "user", "pass");
	 */
	public static AdvanceDBManager sqlServer(String host, int port, String database, String user, String password) {
		String url = "jdbc:sqlserver://" + host + ":" + port + ";databaseName=" + database + ";encrypt=true;trustServerCertificate=true";
		return new AdvanceDBManager(url, user, password);
	}

	/**
	 * Factory method for Oracle connections (using SID).
	 *
	 * Example:
	 *   AdvanceDBManager db = AdvanceDBManager.oracle("localhost", 1521, "ORCL", "user", "pass");
	 */
	public static AdvanceDBManager oracle(String host, int port, String sid, String user, String password) {
		String url = "jdbc:oracle:thin:@" + host + ":" + port + ":" + sid;
		return new AdvanceDBManager(url, user, password);
	}

	/**
	 * Factory method for Oracle connections (using Service Name).
	 *
	 * Example:
	 *   AdvanceDBManager db = AdvanceDBManager.oracleService("localhost", 1521, "myservice", "user", "pass");
	 */
	public static AdvanceDBManager oracleService(String host, int port, String serviceName, String user, String password) {
		String url = "jdbc:oracle:thin:@//" + host + ":" + port + "/" + serviceName;
		return new AdvanceDBManager(url, user, password);
	}

	/**
	 * Returns the detected database type ("PostgreSQL", "MySQL", "SQL Server", "Oracle", or "Unknown").
	 */
	public String getDbType() {
		return dbType;
	}

	private String detectDbType(String url) {
		if (url.startsWith("jdbc:postgresql")) return "PostgreSQL";
		if (url.startsWith("jdbc:mysql")) return "MySQL";
		if (url.startsWith("jdbc:sqlserver")) return "SQL Server";
		if (url.startsWith("jdbc:oracle")) return "Oracle";
		return "Unknown";
	}

	/**
	 * Returns the underlying JDBC connection (for advanced use cases).
	 */
	public Connection getConnection() {
		return connection;
	}

	// ==================== SELECT (Read) ====================

	/**
	 * Executes a SELECT query with optional parameters and returns all rows.
	 * Each row is a Map where keys are column names and values are column values.
	 *
	 * Example:
	 *   List<Map<String, Object>> rows = db.executeQuery("SELECT * FROM users WHERE status = ?", "active");
	 */
	public List<Map<String, Object>> executeQuery(String sql, Object... params) {
		List<Map<String, Object>> results = new ArrayList<>();
		try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
			setParameters(pstmt, params);
			try (ResultSet rs = pstmt.executeQuery()) {
				ResultSetMetaData meta = rs.getMetaData();
				int columnCount = meta.getColumnCount();
				while (rs.next()) {
					Map<String, Object> row = new LinkedHashMap<>();
					for (int i = 1; i <= columnCount; i++) {
						row.put(meta.getColumnLabel(i), rs.getObject(i));
					}
					results.add(row);
				}
			}
		} catch (SQLException e) {
			throw new RuntimeException("Query failed: " + sql + " | Error: " + e.getMessage(), e);
		}
		return results;
	}

	/**
	 * Executes a SELECT query and returns the first row, or null if no results.
	 *
	 * Example:
	 *   Map<String, Object> user = db.executeQueryForSingleRow("SELECT * FROM users WHERE id = ?", 42);
	 */
	public Map<String, Object> executeQueryForSingleRow(String sql, Object... params) {
		List<Map<String, Object>> results = executeQuery(sql, params);
		return results.isEmpty() ? null : results.get(0);
	}

	/**
	 * Executes a SELECT query and returns a single cell value from the first row/column.
	 * Returns null if no results.
	 *
	 * Example:
	 *   String email = (String) db.executeQueryForSingleValue("SELECT email FROM users WHERE id = ?", 42);
	 *   int count = (int) db.executeQueryForSingleValue("SELECT COUNT(*) FROM orders WHERE user_id = ?", 42);
	 */
	public Object executeQueryForSingleValue(String sql, Object... params) {
		Map<String, Object> row = executeQueryForSingleRow(sql, params);
		if (row == null || row.isEmpty()) {
			return null;
		}
		return row.values().iterator().next();
	}

	/**
	 * Returns a single column from all rows as a List.
	 *
	 * Example:
	 *   List<Object> emails = db.executeQueryForColumn("SELECT email FROM users WHERE active = ?", true);
	 */
	public List<Object> executeQueryForColumn(String sql, Object... params) {
		List<Object> column = new ArrayList<>();
		List<Map<String, Object>> rows = executeQuery(sql, params);
		for (Map<String, Object> row : rows) {
			if (!row.isEmpty()) {
				column.add(row.values().iterator().next());
			}
		}
		return column;
	}

	// ==================== INSERT / UPDATE / DELETE (Write) ====================

	/**
	 * Executes an INSERT, UPDATE, or DELETE statement with optional parameters.
	 * Returns the number of affected rows.
	 *
	 * Example:
	 *   int affected = db.executeUpdate("UPDATE users SET status = ? WHERE id = ?", "inactive", 42);
	 */
	public int executeUpdate(String sql, Object... params) {
		try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
			setParameters(pstmt, params);
			return pstmt.executeUpdate();
		} catch (SQLException e) {
			throw new RuntimeException("Update failed: " + sql + " | Error: " + e.getMessage(), e);
		}
	}

	// ==================== Convenience Methods for Test Assertions ====================

	/**
	 * Returns the row count for a given query.
	 *
	 * Example:
	 *   int count = db.getRowCount("SELECT * FROM orders WHERE user_id = ?", 42);
	 *   assertEquals(3, count);
	 */
	public int getRowCount(String sql, Object... params) {
		return executeQuery(sql, params).size();
	}

	/**
	 * Checks if at least one row exists for the given query.
	 *
	 * Example:
	 *   boolean exists = db.recordExists("SELECT 1 FROM users WHERE email = ?", "alice@example.com");
	 *   assertTrue(exists);
	 */
	public boolean recordExists(String sql, Object... params) {
		return !executeQuery(sql, params).isEmpty();
	}

	// ==================== Connection Management ====================

	/**
	 * Closes the database connection. Call this in @AfterEach or @AfterAll.
	 */
	public void close() {
		try {
			if (connection != null && !connection.isClosed()) {
				connection.close();
				System.out.println("Database connection closed.");
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}
	}

	// ==================== Internal Helper ====================

	/**
	 * Sets parameters on a PreparedStatement from a var args array.
	 */
	private void setParameters(PreparedStatement pstmt, Object... params) throws SQLException {
		for (int i = 0; i < params.length; i++) {
			pstmt.setObject(i + 1, params[i]);
		}
	}
}
