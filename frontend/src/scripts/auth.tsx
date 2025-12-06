export const checkUserAccess = async (userId: number): Promise<{
    hasAccess: boolean,
    fullname?: string,
    role?: number
}> => {
    try {
        const response = await fetch(`http://localhost:8000/api/employees/?user_id=${userId}`);

        console.log(response)
        if (response.status === 404) {
            return {hasAccess: false};
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const employee = data.employees?.[0];

        if (employee) {
            return {
                fullname: employee.fullname,
                hasAccess: true,
                role: employee.role
            };
        }

        return {hasAccess: false};
    } catch (error) {
        console.error('Error checking user role:', error);
        return {hasAccess: false};
    }
};