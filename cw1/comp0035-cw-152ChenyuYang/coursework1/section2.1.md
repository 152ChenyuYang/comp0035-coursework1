```mermaid
erDiagram
    AREA {
        string code
        string name
    }
    YEAR {
        int year
    }
    WAITING_LIST {
        int waiting_id
        int year
        string areaCode
        int householdsCount
    }
    AFFORDABLE_HOUSING {
        int housing_id
        int year
        string areaCode
        int housingUnits
    }
    
    AREA ||--o{ WAITING_LIST : "has"
    AREA ||--o{ AFFORDABLE_HOUSING : "provides"
    YEAR ||--o{ WAITING_LIST : "records"
    YEAR ||--o{ AFFORDABLE_HOUSING : "tracks"
    WAITING_LIST ||--o{ AFFORDABLE_HOUSING : "linked"
