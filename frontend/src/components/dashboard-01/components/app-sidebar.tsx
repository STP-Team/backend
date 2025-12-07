"use client"

import * as React from "react"
import {Home} from "lucide-react"

import {NavMain} from "./nav-main"
import {NavUser} from "./nav-user"
import {navigationData} from "@/data/navigation"
import {useAuth} from "@/contexts/AuthContext"
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"

interface AppSidebarProps {
    onNavigate?: (url: string) => void;
    activeContent?: string;
}

export function AppSidebar({
                               onNavigate,
                               activeContent,
                               ...props
                           }: AppSidebarProps & React.ComponentProps<typeof Sidebar>) {
    const {userInfo} = useAuth();

    return (
        <Sidebar collapsible="offcanvas" {...props}>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton
                            asChild
                            className="data-[slot=sidebar-menu-button]:!p-1.5"
                        >
                            <a href="#" onClick={() => onNavigate?.("#dashboard")}>
                                <Home className="!size-5"/>
                                <span className="text-base font-semibold">Админер</span>
                            </a>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                <NavMain
                    navigationData={navigationData}
                    onNavigate={onNavigate}
                    activeContent={activeContent}
                />
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={userInfo}/>
            </SidebarFooter>
        </Sidebar>
    )
}