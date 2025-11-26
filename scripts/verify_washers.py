import asyncio
import httpx
import sys

BASE_URL = "http://localhost:8000/api/v1/washing/washers"

async def run_verification():
    async with httpx.AsyncClient() as client:
        print(f"Checking API health at http://localhost:8000/health ...")
        try:
            resp = await client.get("http://localhost:8000/health")
            if resp.status_code != 200:
                print(f"❌ API is not healthy: {resp.status_code}")
                return
            print("✅ API is healthy")
        except Exception as e:
            print(f"❌ Could not connect to API: {e}")
            print("Make sure the backend is running (docker-compose up -d)")
            return

        # 1. Create Washer
        print("\n1. Creating Washer...")
        import random
        rand_id = random.randint(1000, 9999)
        new_washer = {
            "full_name": "John Doe",
            "email": f"john.doe.{rand_id}@example.com",
            "phone": "1234567890",
            "commission_percentage": 50,
            "password": "securepassword123"
        }
        resp = await client.post(f"{BASE_URL}/", json=new_washer)
        if resp.status_code != 200:
            print(f"❌ Failed to create washer: {resp.text}")
            return
        created_washer = resp.json()
        print(f"✅ Created: {created_washer}")
        washer_id = created_washer["id"]

        # 2. List Washers
        print("\n2. Listing Washers...")
        resp = await client.get(f"{BASE_URL}/")
        washers = resp.json()
        print(f"✅ Found {len(washers)} washers")
        found = any(w["id"] == washer_id for w in washers)
        if not found:
            print("❌ Created washer not found in list")
            return

        # 3. Get Washer
        print(f"\n3. Getting Washer {washer_id}...")
        resp = await client.get(f"{BASE_URL}/{washer_id}")
        if resp.status_code != 200:
            print(f"❌ Failed to get washer: {resp.text}")
            return
        print(f"✅ Got: {resp.json()}")

        # 4. Update Washer
        print(f"\n4. Updating Washer {washer_id}...")
        update_data = {
            "full_name": "John Updated",
            "commission_percentage": 60
        }
        resp = await client.put(f"{BASE_URL}/{washer_id}", json=update_data)
        if resp.status_code != 200:
            print(f"❌ Failed to update washer: {resp.text}")
            return
        updated_washer = resp.json()
        print(f"✅ Updated: {updated_washer}")
        if updated_washer["full_name"] != "John Updated":
            print("❌ Name was not updated")
            return

        # 5. Delete Washer
        print(f"\n5. Deleting Washer {washer_id}...")
        resp = await client.delete(f"{BASE_URL}/{washer_id}")
        if resp.status_code != 200:
            print(f"❌ Failed to delete washer: {resp.text}")
            return
        print("✅ Deleted")

        # Verify deletion
        resp = await client.get(f"{BASE_URL}/{washer_id}")
        if resp.status_code == 404:
            print("✅ Verification successful: Washer is gone")
        else:
            print("❌ Washer still exists after deletion")

if __name__ == "__main__":
    try:
        asyncio.run(run_verification())
    except KeyboardInterrupt:
        pass
