import { ICepConfig } from "../types";

export function joinManifest(config: ICepConfig) {
    const { id, version, extensionVersion, requiredRuntimeVersion, hosts, parameters, panels } = config
    const mainId=`${id}`
    const panel = panels[0]
    return `<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<ExtensionManifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ExtensionBundleId="${id}.body" ExtensionBundleVersion="1.0" Version="6.0"> <!-- MAJOR-VERSION-UPDATE-MARKER -->
    <ExtensionList>
        <Extension Id="${mainId}" Version="${extensionVersion}"/>
    </ExtensionList>
    <ExecutionEnvironment>
        <HostList>
            ${hosts.map(item => `<Host Name="${item.name}" Version="${item.version}"/>`).join("\n")}
        </HostList>
        <LocaleList>
            <Locale Code="All"/>
        </LocaleList>
        <RequiredRuntimeList>
            <RequiredRuntime Name="CSXS" Version="${requiredRuntimeVersion}"/> <!-- MAJOR-VERSION-UPDATE-MARKER -->
        </RequiredRuntimeList>
    </ExecutionEnvironment>
    <DispatchInfoList>
        <Extension Id="${mainId}">
            <DispatchInfo>
                <Resources>
                    <MainPath>./index.html</MainPath>
					<!-- <ScriptPath>./jsx/core.jsx</ScriptPath> -->
                    <CEFCommandLine>
                        ${parameters.map(item => `<Parameter>${item}</Parameter>`).join("\n")}
                    </CEFCommandLine>
                </Resources>
                <Lifecycle>
                    <AutoVisible>true</AutoVisible>
                </Lifecycle>
                <UI>
                    <Type>Panel</Type>
                    <Menu>${panel.displayName}</Menu>
                    <Geometry>
                        <Size>
                            <Height>${panel.height}</Height>
                            <Width>${panel.width}</Width>
                        </Size>
                        <MaxSize>
                            <Height>${panel.maxHeight||panel.height}</Height>
                            <Width>${panel.maxWidth||panel.width}</Width>
                        </MaxSize>
                        <MinSize>
                            <Height>${panel.minHeight||panel.height}</Height>
                            <Width>${panel.minWidth||panel.width}</Width>
                        </MinSize>
                    </Geometry>
                    <Icons>
                        <Icon Type="Normal">./img/highlight.png</Icon>
                        <Icon Type="RollOver">./img/dark.png</Icon>
                        <Icon Type="DarkNormal">./img/highlight.png</Icon>
                        <Icon Type="DarkRollOver">./img/dark.png</Icon>
                    </Icons>
                </UI>
            </DispatchInfo>
        </Extension>
    </DispatchInfoList>
</ExtensionManifest>

    `
}