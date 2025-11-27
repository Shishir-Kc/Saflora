def check_address(province_id, area_id) -> bool:
    from Accounts.models import Province, Location
    
    location = Location.objects.get(id=area_id)
    province = Province.objects.get(id=province_id)

    valid_area_koshi = [f"itahari-{i}" for i in range(1, 21)]

    if province.name == "Koshi":
        return location.name in valid_area_koshi
    else:
        return location.name not in valid_area_koshi