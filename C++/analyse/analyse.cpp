#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <iomanip>

// Define the table structure
struct Table {
    std::vector<std::string> columns;
    std::vector<std::vector<std::string>> rows;
};

// Define the history record structure
struct HistoryRecord {
    std::string databaseName;
    std::string tableName;
    std::string operation;
    std::string details;
};

// Define the database structure
class Database {
private:
    std::unordered_map<std::string, Table> tables;

    // Calculate the maximum width of each column
    std::vector<size_t> calculateMaxWidths(const Table& table) {
        std::vector<size_t> maxWidths(table.columns.size(), 0);
        for (size_t i = 0; i < table.columns.size(); ++i) {
            maxWidths[i] = table.columns[i].size();
        }
        for (const auto& row : table.rows) {
            for (size_t i = 0; i < row.size(); ++i) {
                maxWidths[i] = std::max(maxWidths[i], row[i].size());
            }
        }
        return maxWidths;
    }

public:
    // Create a table
    void createTable(const std::string& tableName, const std::vector<std::string>& columns) {
        if (tables.find(tableName) != tables.end()) {
            std::cout << "Table " << tableName << " already exists." << std::endl;
            return;
        }
        Table newTable;
        newTable.columns = columns;
        tables[tableName] = newTable;
        std::cout << "Table " << tableName << " created successfully." << std::endl;
    }

    // Drop a table
    void dropTable(const std::string& tableName) {
        auto it = tables.find(tableName);
        if (it == tables.end()) {
            std::cout << "Table " << tableName << " does not exist." << std::endl;
            return;
        }
        tables.erase(it);
        std::cout << "Table " << tableName << " dropped successfully." << std::endl;
    }

    // Insert data
    void insertData(const std::string& tableName, const std::vector<std::string>& values) {
        auto it = tables.find(tableName);
        if (it == tables.end()) {
            std::cout << "Table " << tableName << " does not exist." << std::endl;
            return;
        }
        Table& table = it->second;
        if (values.size() != table.columns.size()) {
            std::cout << "The number of columns in the inserted data does not match the table structure." << std::endl;
            return;
        }
        table.rows.push_back(values);
        std::cout << "Data inserted successfully." << std::endl;
    }

    // Select data
    void selectData(const std::string& tableName) {
        auto it = tables.find(tableName);
        if (it == tables.end()) {
            std::cout << "Table " << tableName << " does not exist." << std::endl;
            return;
        }
        Table& table = it->second;
        std::vector<size_t> maxWidths = calculateMaxWidths(table);

        // Output the table header
        for (size_t i = 0; i < table.columns.size(); ++i) {
            std::cout << std::left << std::setw(maxWidths[i] + 2) << table.columns[i];
        }
        std::cout << std::endl;

        // Output the data rows
        for (const auto& row : table.rows) {
            for (size_t i = 0; i < row.size(); ++i) {
                std::cout << std::left << std::setw(maxWidths[i] + 2) << row[i];
            }
            std::cout << std::endl;
        }
    }

    // Update data
    void updateData(const std::string& tableName, const std::string& conditionColumn, const std::string& conditionValue, const std::string& updateColumn, const std::string& updateValue) {
        auto it = tables.find(tableName);
        if (it == tables.end()) {
            std::cout << "Table " << tableName << " does not exist." << std::endl;
            return;
        }
        Table& table = it->second;
        int conditionColumnIndex = -1;
        int updateColumnIndex = -1;
        for (size_t i = 0; i < table.columns.size(); ++i) {
            if (table.columns[i] == conditionColumn) {
                conditionColumnIndex = static_cast<int>(i);
            }
            if (table.columns[i] == updateColumn) {
                updateColumnIndex = static_cast<int>(i);
            }
        }
        if (conditionColumnIndex == -1 || updateColumnIndex == -1) {
            std::cout << "The specified column name does not exist." << std::endl;
            return;
        }
        bool updated = false;
        for (auto& row : table.rows) {
            if (row[conditionColumnIndex] == conditionValue) {
                row[updateColumnIndex] = updateValue;
                updated = true;
            }
        }
        if (updated) {
            std::cout << "Data updated successfully." << std::endl;
        } else {
            std::cout << "No data matching the condition was found." << std::endl;
        }
    }

    // Export the table to a file
    void exportTableToFile(const std::string& tableName, const std::string& filename) {
        auto it = tables.find(tableName);
        if (it == tables.end()) {
            std::cout << "Table " << tableName << " does not exist." << std::endl;
            return;
        }
        Table& table = it->second;
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cout << "Unable to open file " << filename << " for writing." << std::endl;
            return;
        }
        std::vector<size_t> maxWidths = calculateMaxWidths(table);

        // Write the table header
        for (size_t i = 0; i < table.columns.size(); ++i) {
            file << std::left << std::setw(maxWidths[i] + 2) << table.columns[i];
        }
        file << std::endl;

        // Write the data rows
        for (const auto& row : table.rows) {
            for (size_t i = 0; i < row.size(); ++i) {
                file << std::left << std::setw(maxWidths[i] + 2) << row[i];
            }
            file << std::endl;
        }
        file.close();
        std::cout << "Table " << tableName << " has been successfully exported to file " << filename << std::endl;
    }
};

// Define the database management system
class DBMS {
private:
    std::unordered_map<std::string, Database> databases;
    std::string currentDatabase;
    std::vector<HistoryRecord> history;

    // Record the historical operation
    void recordHistory(const std::string& tableName, const std::string& operation, const std::string& details) {
        HistoryRecord record;
        record.databaseName = currentDatabase;
        record.tableName = tableName;
        record.operation = operation;
        record.details = details;
        history.push_back(record);
    }

public:
    // Create a database
    void createDatabase(const std::string& dbName) {
        if (databases.find(dbName) != databases.end()) {
            std::cout << "Database " << dbName << " already exists." << std::endl;
            return;
        }
        databases[dbName] = Database();
        std::cout << "Database " << dbName << " created successfully." << std::endl;
        recordHistory("", "CREATE DATABASE", dbName);
    }

    // Use a database
    void useDatabase(const std::string& dbName) {
        if (databases.find(dbName) == databases.end()) {
            std::cout << "Database " << dbName << " does not exist." << std::endl;
            return;
        }
        currentDatabase = dbName;
        std::cout << "Switched to database " << dbName << std::endl;
        recordHistory("", "USE DATABASE", dbName);
    }

    // Create a table
    void createTable(const std::string& tableName, const std::vector<std::string>& columns) {
        if (currentDatabase.empty()) {
            std::cout << "Please select a database first." << std::endl;
            return;
        }
        databases[currentDatabase].createTable(tableName, columns);
        std::stringstream ss;
        for (const auto& col : columns) {
            ss << col << " ";
        }
        recordHistory(tableName, "CREATE TABLE", ss.str());
    }

    // Drop a table
    void dropTable(const std::string& tableName) {
        if (currentDatabase.empty()) {
            std::cout << "Please select a database first." << std::endl;
            return;
        }
        databases[currentDatabase].dropTable(tableName);
        recordHistory(tableName, "DROP TABLE", "");
    }

    // Insert data
    void insertData(const std::string& tableName, const std::vector<std::string>& values) {
        if (currentDatabase.empty()) {
            std::cout << "Please select a database first." << std::endl;
            return;
        }
        databases[currentDatabase].insertData(tableName, values);
        std::stringstream ss;
        for (const auto& val : values) {
            ss << val << " ";
        }
        recordHistory(tableName, "INSERT INTO", ss.str());
    }

    // Select data
    void selectData(const std::string& tableName) {
        if (currentDatabase.empty()) {
            std::cout << "Please select a database first." << std::endl;
            return;
        }
        databases[currentDatabase].selectData(tableName);
        recordHistory(tableName, "SELECT FROM", "");
    }

    // Update data
    void updateData(const std::string& tableName, const std::string& conditionColumn, const std::string& conditionValue, const std::string& updateColumn, const std::string& updateValue) {
        if (currentDatabase.empty()) {
            std::cout << "Please select a database first." << std::endl;
            return;
        }
        databases[currentDatabase].updateData(tableName, conditionColumn, conditionValue, updateColumn, updateValue);
        std::string details = "Condition: " + conditionColumn + " = " + conditionValue + ", Update: " + updateColumn + " = " + updateValue;
        recordHistory(tableName, "UPDATE", details);
    }

    // Export the table to a file
    void exportTableToFile(const std::string& tableName, const std::string& filename) {
        if (currentDatabase.empty()) {
            std::cout << "Please select a database first." << std::endl;
            return;
        }
        databases[currentDatabase].exportTableToFile(tableName, filename);
        recordHistory(tableName, "EXPORT TABLE", filename);
    }

    // Show the history records
    void showHistory() {
        std::cout << "Data change history records:" << std::endl;
        for (const auto& record : history) {
            std::cout << "Database: " << record.databaseName << ", Table: " << record.tableName << ", Operation: " << record.operation << ", Details: " << record.details << std::endl;
        }
    }
};

// Parse user input
std::vector<std::string> parseInput(const std::string& input) {
    std::vector<std::string> tokens;
    std::istringstream iss(input);
    std::string token;
    while (iss >> token) {
        tokens.push_back(token);
    }
    return tokens;
}

int main() {
    DBMS dbms;
    std::string input;

    while (true) {
        std::cout << "DBMS> ";
        std::getline(std::cin, input);
        std::vector<std::string> tokens = parseInput(input);

        if (tokens.empty()) continue;

        if (tokens[0] == "CREATE" && tokens[1] == "DATABASE") {
            if (tokens.size() != 3) {
                std::cout << "Syntax error: CREATE DATABASE requires a database name." << std::endl;
                continue;
            }
            dbms.createDatabase(tokens[2]);
        } else if (tokens[0] == "USE") {
            if (tokens.size() != 2) {
                std::cout << "Syntax error: USE requires a database name." << std::endl;
                continue;
            }
            dbms.useDatabase(tokens[1]);
        } else if (tokens[0] == "CREATE" && tokens[1] == "TABLE") {
            if (tokens.size() < 3) {
                std::cout << "Syntax error: CREATE TABLE requires a table name and column names." << std::endl;
                continue;
            }
            std::string tableName = tokens[2];
            std::vector<std::string> columns(tokens.begin() + 3, tokens.end());
            dbms.createTable(tableName, columns);
        } else if (tokens[0] == "DROP" && tokens[1] == "TABLE") {
            if (tokens.size() != 3) {
                std::cout << "Syntax error: DROP TABLE requires a table name." << std::endl;
                continue;
            }
            dbms.dropTable(tokens[2]);
        } else if (tokens[0] == "INSERT" && tokens[1] == "INTO") {
            if (tokens.size() < 4) {
                std::cout << "Syntax error: INSERT INTO requires a table name and values." << std::endl;
                continue;
            }
            std::string tableName = tokens[2];
            std::vector<std::string> values(tokens.begin() + 3, tokens.end());
            dbms.insertData(tableName, values);
        } else if (tokens[0] == "SELECT" && tokens[1] == "FROM") {
            if (tokens.size() != 3) {
                std::cout << "Syntax error: SELECT FROM requires a table name." << std::endl;
                continue;
            }
            dbms.selectData(tokens[2]);
        } else if (tokens[0] == "UPDATE") {
            if (tokens.size() != 6) {
                std::cout << "Syntax error: UPDATE requires a table name, condition column, condition value, update column, and update value." << std::endl;
                continue;
            }
            std::string tableName = tokens[1];
            std::string conditionColumn = tokens[2];
            std::string conditionValue = tokens[3];
            std::string updateColumn = tokens[4];
            std::string updateValue = tokens[5];
            dbms.updateData(tableName, conditionColumn, conditionValue, updateColumn, updateValue);
        } else if (tokens[0] == "EXPORT" && tokens[1] == "TABLE") {
            if (tokens.size() != 4) {
                std::cout << "Syntax error: EXPORT TABLE requires a table name and a file name." << std::endl;
                continue;
            }
            std::string tableName = tokens[2];
            std::string filename = tokens[3];
            dbms.exportTableToFile(tableName, filename);
        } else if (tokens[0] == "SHOW" && tokens[1] == "HISTORY") {
            dbms.showHistory();
        } else if (tokens[0] == "EXIT") {
            break;
        } else {
            std::cout << "Unknown command, please try again." << std::endl;
        }
    }

    return 0;
}