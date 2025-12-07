import {TrendingUp} from "lucide-react"
import {useEffect, useState} from "react"

import {Badge} from "@/components/ui/badge"
import {Card, CardDescription, CardFooter, CardHeader, CardTitle,} from "@/components/ui/card"
import {getCookie} from "@/lib/utils"

export function SectionCards() {
    const [employeeCount, setEmployeeCount] = useState<number | null>(null)
    const [achievementsCount, setAchievementsCount] = useState<number | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const token = getCookie('access_token');

        const fetchEmployees = async () => {
            try {
                const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

                const headers: HeadersInit = {
                    'Content-Type': 'application/json',
                };

                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }

                const response = await fetch(`${apiBaseUrl}/api/v1/employees/`, {
                    headers
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json()
                setEmployeeCount(data.employees.length)
            } catch (error) {
                console.error('Error fetching employees:', error)
                setEmployeeCount(0)
            } finally {
                setLoading(false)
            }
        }

        const fetchAchievements = async () => {
            try {
                const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;

                const headers: HeadersInit = {
                    'Content-Type': 'application/json',
                };

                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }

                const response = await fetch(`${apiBaseUrl}/api/v1/achievements/`, {
                    headers
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json()
                console.log(data)
                const count = data.achievements.length
                setAchievementsCount(count)
            } catch (error) {
                console.error('Error fetching achievements:', error)
                setAchievementsCount(0)
            } finally {
                setLoading(false)
            }
        }
        fetchEmployees()
        fetchAchievements()
    }, [])
    return (
        <div className="grid grid-cols-1 gap-4 px-4 lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
            <Card className="@container/card">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardDescription>Всего сотрудников</CardDescription>
                        <Badge variant="outline">
                            <TrendingUp className="size-3"/>
                            {loading ? "..." : "Актуально"}
                        </Badge>
                    </div>
                    <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
                        {loading ? "Загрузка..." : employeeCount || 0}
                    </CardTitle>
                </CardHeader>
                <CardFooter className="flex-col items-start gap-1.5 text-sm">
                    <div className="line-clamp-1 flex gap-2 font-medium">
                        Общее количество сотрудников <TrendingUp className="size-4"/>
                    </div>
                    <div className="text-muted-foreground">
                        Данные обновляются в реальном времени
                    </div>
                </CardFooter>
            </Card>

            <Card className="@container/card">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardDescription>Всего достижений</CardDescription>
                        <Badge variant="outline">
                            <TrendingUp className="size-3"/>
                            {loading ? "..." : "Актуально"}
                        </Badge>
                    </div>
                    <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
                        {loading ? "Загрузка..." : achievementsCount || 0}
                    </CardTitle>
                </CardHeader>
                <CardFooter className="flex-col items-start gap-1.5 text-sm">
                    <div className="line-clamp-1 flex gap-2 font-medium">
                        Общее количество достижений <TrendingUp className="size-4"/>
                    </div>
                    <div className="text-muted-foreground">
                        Данные обновляются в реальном времени
                    </div>
                </CardFooter>
            </Card>

            <Card className="@container/card">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardDescription>Активные аккаунты</CardDescription>
                        <Badge variant="outline">
                            <TrendingUp className="size-3"/>
                            +8.2%
                        </Badge>
                    </div>
                    <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
                        45,678
                    </CardTitle>
                </CardHeader>
                <CardFooter className="flex-col items-start gap-1.5 text-sm">
                    <div className="line-clamp-1 flex gap-2 font-medium">
                        Высокая активность пользователей <TrendingUp className="size-4"/>
                    </div>
                    <div className="text-muted-foreground">Превышают целевые показатели</div>
                </CardFooter>
            </Card>

            <Card className="@container/card">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardDescription>Темп роста</CardDescription>
                        <Badge variant="outline">
                            <TrendingUp className="size-3"/>
                            +4.5%
                        </Badge>
                    </div>
                    <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
                        4.5%
                    </CardTitle>
                </CardHeader>
                <CardFooter className="flex-col items-start gap-1.5 text-sm">
                    <div className="line-clamp-1 flex gap-2 font-medium">
                        Стабильный рост производительности <TrendingUp className="size-4"/>
                    </div>
                    <div className="text-muted-foreground">Соответствует прогнозам роста</div>
                </CardFooter>
            </Card>
        </div>
    )
}