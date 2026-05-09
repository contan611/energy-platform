import random

# [1] HTML의 regions 배열과 동일한 데이터
REGIONS = [
    "서울 강남구","서울 강동구","서울 강북구","서울 강서구","서울 관악구","서울 광진구","서울 구로구","서울 금천구","서울 노원구","서울 도봉구","서울 동대문구","서울 동작구","서울 마포구","서울 서대문구","서울 서초구","서울 성동구","서울 성북구","서울 송파구","서울 양천구","서울 영등포구","서울 용산구","서울 은평구","서울 종로구","서울 중구","서울 중랑구",
    "경기 수원시","경기 용인시","경기 고양시","경기 화성시","경기 성남시","경기 부천시","경기 남양주시","경기 안산시","경기 평택시","경기 안양시","경기 시흥시","경기 파주시","경기 김포시","경기 의정부시","경기 광주시","경기 하남시","경기 군포시","경기 오산시","경기 양주시","경기 이천시","경기 구리시","경기 안성시","경기 포천시","경기 의왕시",
    "전북 전주시","전북 익산시","전북 군산시","전북 정읍시","전북 남원시","전북 김제시","전북 완주군","전북 고창군","전북 부안군","전북 순창군","전북 임실군","전북 무주군","전북 진안군","전북 장수군",
    "부산 중구","부산 해운대구","부산 사하구","부산 연제구","부산 수영구","인천 서구","인천 연수구","대구 수성구","광주 광산구","대전 유성구","울산 남구","세종특별자치시","제주 제주시"
]

# [2] HTML의 generateRegionalData 함수와 동일한 로직
def generate_regional_data(region, year):
    base = 1200
    if any(r in region for r in ["강남", "화성", "수원"]):
        base = 3800
    elif "시" in region:
        base = 2100
    
    growth = 1 + (year - 2023) * 0.054
    # 월별 가중치 리스트
    weights = [1.3, 1.1, 0.9, 0.8, 0.9, 1.4, 1.7, 1.9, 1.3, 0.9, 1.1, 1.4]
    
    # 데이터 생성 (랜덤 오차 포함)
    return [round(base * m * growth + random.uniform(0, 80)) for m in weights]

# [3] HTML의 generateAiResponse 함수와 동일한 답변 로직
def generate_ai_response(query, region, year, current_data):
    data_sum = sum(current_data)
    peak = max(current_data)
    peak_month = current_data.index(peak) + 1

    if "패턴" in query or "특징" in query:
        return f"{region}의 전력 사용 패턴을 분석해 보았습니다. 이 지역은 현재 연간 약 {data_sum:,} MWh의 소비량을 보이고 있으며, {peak_month}월에 최대 부하({peak:,} MWh)가 발생하는 특징이 있습니다. 이는 전형적인 냉난방 부하 중심의 에너지 소비 구조를 나타냅니다."
    elif any(word in query for word in ["2030", "전망", "미래"]):
        return f"{year}년 이후의 {region} 전망을 분석하자면, 분산 에너지 활성화 정책에 따라 에너지 자립도가 약 12% 향상될 것으로 예측됩니다. 특히 2030년 예상 데이터에 따르면 전기차(EV) 충전 부하가 전체 전력량의 약 18%를 차지하며 새로운 피크 시점을 형성할 가능성이 높습니다."
    elif "절약" in query or "효율" in query:
        return f"{region}의 효율 개선을 위해 Gemini는 {peak_month}월 피크 관리를 추천합니다. 해당 기간에 에너지 저장 시스템(ESS)을 도입한다면 연간 약 8.5%의 전력 구입 비용을 절감할 수 있을 것으로 분석됩니다."
    else:
        return f"질문하신 '{query}'에 대해 {region}의 데이터를 기반으로 고찰해 보았습니다. 현재 {year}년 시계열 상에서 이 지역은 탄소 배출 저감율 3.2%를 기록 중이며, 전력 수급 안정성은 '매우 우수' 등급입니다."

# [4] 메인 실행부 (HTML의 UI 흐름을 터미널로 구현)
def main():
    print("=== WP ENERGY GEMINI ANALYTICS (Python Ver.) ===")
    
    # 1. 지역 검색 (HTML의 searchRegion 기능)
    search_term = input("지역명을 입력하세요 (예: 익산): ")
    filtered_regions = [r for r in REGIONS if search_term in r]
    
    if not filtered_regions:
        print("검색 결과가 없습니다.")
        return
    
    print("\n[검색 결과]")
    for i, r in enumerate(filtered_regions[:10]):
        print(f"{i+1}. {r}")
    
    choice = int(input("\n지역 번호를 선택하세요: ")) - 1
    selected_region = filtered_regions[choice]
    
    # 2. 연도 선택 (HTML의 setYear 기능)
    selected_year = int(input("분석할 연도를 입력하세요 (2023~2030): "))
    
    # 3. 데이터 생성 및 출력 (HTML의 updateAll 및 차트 데이터)
    current_chart_data = generate_regional_data(selected_region, selected_year)
    
    print(f"\n>>> {selected_region} ({selected_year}년) 분석 데이터 로드 완료")
    print(f"월별 데이터(MWh): {current_chart_data}")
    print(f"연간 총 사용량: {sum(current_chart_data):,} MWh")
    
    # 4. AI 질문 답변 (HTML의 askGemini 기능)
    while True:
        query = input("\nAI Analyst에게 질문하세요 (종료: q): ")
        if query.lower() == 'q': break
        
        response = generate_ai_response(query, selected_region, selected_year, current_chart_data)
        print(f"\n[Gemini]: {response}")

if __name__ == "__main__":
    main()