from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "customers" (
    "Id" UUID NOT NULL PRIMARY KEY,
    "OrderNumber" INT NOT NULL,
    "UserNumber" INT NOT NULL,
    "ObjCustName" VARCHAR(255) NOT NULL,
    "ObjCustTitle" VARCHAR(255) NOT NULL,
    "ObjCustPhone1" VARCHAR(50) NOT NULL,
    "ObjCustPhone2" VARCHAR(50),
    "ObjCustPhone3" VARCHAR(50),
    "ObjCustPhone4" VARCHAR(50),
    "ObjCustPhone5" VARCHAR(50),
    "ObjCustAddress" TEXT NOT NULL,
    "IsVisibleInCabinet" BOOL NOT NULL DEFAULT True,
    "ReclosingRequest" BOOL NOT NULL DEFAULT False,
    "ReclosingFailure" BOOL NOT NULL DEFAULT False,
    "PINCode" VARCHAR(50) NOT NULL,
    "LastSync" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "security_objects" (
    "Id" UUID NOT NULL PRIMARY KEY,
    "AccountNumber" INT NOT NULL,
    "CloudObjectID" INT NOT NULL,
    "Name" VARCHAR(255) NOT NULL,
    "ObjectPassword" VARCHAR(255) NOT NULL,
    "Address" TEXT NOT NULL,
    "Phone1" VARCHAR(50) NOT NULL,
    "Phone2" VARCHAR(50),
    "TypeName" VARCHAR(100) NOT NULL,
    "IsFire" BOOL NOT NULL,
    "IsArm" BOOL NOT NULL,
    "IsPanic" BOOL NOT NULL,
    "DeviceTypeName" VARCHAR(100) NOT NULL,
    "EventTemplateName" VARCHAR(100) NOT NULL,
    "ContractNumber" VARCHAR(100) NOT NULL,
    "ContractPrice" DECIMAL(10,2) NOT NULL,
    "MoneyBalance" DECIMAL(10,2) NOT NULL,
    "PaymentDate" TIMESTAMPTZ NOT NULL,
    "DebtInformLevel" INT NOT NULL,
    "Disabled" BOOL NOT NULL,
    "DisableReason" INT NOT NULL,
    "DisableDate" TIMESTAMPTZ NOT NULL,
    "AutoEnable" BOOL NOT NULL,
    "AutoEnableDate" TIMESTAMPTZ NOT NULL,
    "CustomersComment" TEXT NOT NULL,
    "CommentForOperator" TEXT NOT NULL,
    "CommentForGuard" TEXT NOT NULL,
    "MapFileName" VARCHAR(255) NOT NULL,
    "WebLink" VARCHAR(255) NOT NULL,
    "ControlTime" INT NOT NULL,
    "CTIgnoreSystemEvent" BOOL NOT NULL,
    "IsStateArm" BOOL NOT NULL,
    "IsStateAlarm" BOOL NOT NULL,
    "IsStatePartArm" BOOL NOT NULL,
    "StateArmDisArmDateTime" TIMESTAMPTZ NOT NULL,
    "LastSync" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
