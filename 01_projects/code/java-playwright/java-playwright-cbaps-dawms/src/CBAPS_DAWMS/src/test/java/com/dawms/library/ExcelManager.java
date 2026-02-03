package com.dawms.library;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Utility class for reading test data from Excel files.
 */
public class ExcelManager {

    private Workbook workbook;
    private Sheet sheet;

    public ExcelManager(String filePath, String sheetName) throws IOException {
        FileInputStream fis = new FileInputStream(filePath);
        workbook = new XSSFWorkbook(fis);
        sheet = workbook.getSheet(sheetName);
        fis.close();
    }

    public int getRowCount() {
        return sheet.getLastRowNum();
    }

    public int getColumnCount() {
        return sheet.getRow(0).getLastCellNum();
    }

    public String getCellData(int rowNum, int colNum) {
        Row row = sheet.getRow(rowNum);
        if (row == null) return "";
        Cell cell = row.getCell(colNum);
        if (cell == null) return "";

        DataFormatter formatter = new DataFormatter();
        return formatter.formatCellValue(cell);
    }

    public Object[][] getTestData() {
        int rowCount = getRowCount();
        int colCount = getColumnCount();
        Object[][] data = new Object[rowCount][colCount];

        for (int i = 1; i <= rowCount; i++) {
            for (int j = 0; j < colCount; j++) {
                data[i - 1][j] = getCellData(i, j);
            }
        }
        return data;
    }

    public List<String[]> getTestDataAsList() {
        List<String[]> data = new ArrayList<>();
        int rowCount = getRowCount();
        int colCount = getColumnCount();

        for (int i = 1; i <= rowCount; i++) {
            String[] rowData = new String[colCount];
            for (int j = 0; j < colCount; j++) {
                rowData[j] = getCellData(i, j);
            }
            data.add(rowData);
        }
        return data;
    }

    public void close() throws IOException {
        if (workbook != null) {
            workbook.close();
        }
    }
}
