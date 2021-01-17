//
//  main.c
//  Options_db
//
//  Created by Sato on 12/21/20.
//

#include <stdio.h>
#include <sqlite3.h>

int callback(void *, int, char **, char **);

int main(void)
{
    // Dec 2020 -> Dec 2021
    int days[13][24] = {
        {1,2,3,4,7,8,9,10,11,14,15,16,17,18,21,22,23},
        {4,5,6,7,8,11,12,13,14,15,19,20,21,22,25,26,27,28,29},
        {1,2,3,4,5,8,9,10,11,12,16,17,18,19,22,23,24,25,26},
        {1,2,3,4,5,8,9,10,11,12,15,16,17,18,19,22,23,24,25,26,29,30,31},
        {5,6,7,8,9,12,13,14,15,16,19,20,21,22,23,26,27,28,29,30},
        {3,4,5,6,7,10,11,12,13,14,17,18,19,20,21,24,25,26,27,28},
        {1,2,3,4,7,8,9,10,11,14,15,16,17,18,21,22,23,24,25,28,29,30},
        {1,2,6,7,8,9,12,13,14,15,16,19,20,21,22,23,26,27,28,29,30},
        {2,3,4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26,27,30,31},
        {1,2,3,7,8,9,10,13,14,15,16,17,20,21,22,23,24,27,28,29,30},
        {1,4,5,6,7,8,12,13,14,15,18,19,20,21,22,25,26,27,28,29},
        {1,2,3,4,5,8,9,10,12,15,16,17,18,19,22,23,24,29,30},
        {1,2,3,6,7,8,9,10,13,14,15,16,17,20,21,22,27,28,29,30}
    };
    
    int current_day = days[0][16];
    
    if(current_day > 0){
        printf("here");
    }
    
    sqlite3* db;
    char* err_msg = 0;
    
    int rc = sqlite3_open("/Users/Sato/Documents/PycharmProjects/Tsuru/Options_temp.db", &db);
    
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Cnat connect: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        
        return 1;
    }
    
    char* sql = "SELECT * FROM puts";
    
    rc = sqlite3_exec(db, sql, callback, 0, &err_msg);
    
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQL error: %s\n", err_msg);
        
        sqlite3_free(err_msg);
        sqlite3_close(db);
        
        return 1;
    }
    sqlite3_close(db);
    
    return 0;
}

int callback(void* NotUsed, int argc, char **argv, char **azColName)
{
    NotUsed = 0;
    
    for (int i = 0; i < argc; i++)
    {
        printf("%s,", argv[i]);
        // printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
        
    }
    printf("\n");
    
    return 0;
}
