import asyncio
from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

app = FastAPI(title="Async Square Calculator")


class CalculateRequest(BaseModel):
    numbers: list[float] = Field(min_length=1)
    delays: list[float] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_input(self):
        if len(self.numbers) != len(self.delays):
            raise ValueError("The numbers and delays lists must have the same length")
        if any(delay < 0 for delay in self.delays):
            raise ValueError("Delays must be non-negative")
        return self


class CalculationResult(BaseModel):
    number: float
    square: float
    delay: float
    time: float


class CalculateResponse(BaseModel):
    results: list[CalculationResult]
    total_time: float
    parallel_faster_than_sequential: bool


async def calculate_square(number: float, delay: float) -> CalculationResult:
    start = perf_counter()
    await asyncio.sleep(delay)
    elapsed = perf_counter() - start
    return CalculationResult(
        number=number,
        square=number**2,
        delay=delay,
        time=round(elapsed, 2),
    )


@app.post("/calculate/", response_model=CalculateResponse)
async def calculate(data: CalculateRequest) -> CalculateResponse:
    start = perf_counter()
    tasks = (
        calculate_square(number, delay)
        for number, delay in zip(data.numbers, data.delays)
    )
    results = await asyncio.gather(*tasks)
    total_time = perf_counter() - start
    sequential_time = sum(data.delays)
    return CalculateResponse(
        results=list(results),
        total_time=round(total_time, 2),
        parallel_faster_than_sequential=total_time < sequential_time,
    )
