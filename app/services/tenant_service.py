from app.db.models import Tenant


class TenantService:
    async def create_tenant(self, db, data):
        tenant = Tenant(name=data.name)

        try:
            db.add(tenant)
            await db.commit()
            await db.refresh(tenant)
            return tenant

        except Exception:
            await db.rollback()
            raise