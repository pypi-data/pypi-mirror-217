import pytest
from onlinepvt.models import CalculationComposition, ProblemDetails 
from onlinepvt.online_pvt_client import OnlinePvtClient
from onlinepvt.demofluids.fluids import nHexane_Ethylene_HDPE7

@pytest.mark.asyncio
async def test_call_flash():
    client = OnlinePvtClient(
      "https://localhost:5201", "CEAB3F14-EE16-492D-9551-02A4D19EAC98", "##glD47#al!=(d+53ES3?qW") # "https://api.onlinepvt.com", "UserId", "AccessSecret")

    input = client.get_flash_input()
    input.temperature = 445
    input.pressure = 20
    input.components = [
        CalculationComposition(mass=0.78),
        CalculationComposition(mass=0.02),
        CalculationComposition(mass=0.20)
    ]
    input.flash_type = "Fixed Temperature/Pressure"

    input.fluid = nHexane_Ethylene_HDPE7()
    input.units = "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"

    result: ProblemDetails = await client.call_flash_async(input)

    await client.cleanup()

    #assert result.status == 400
    assert result.api_status == True
    assert len(result.point.phases) == 4
