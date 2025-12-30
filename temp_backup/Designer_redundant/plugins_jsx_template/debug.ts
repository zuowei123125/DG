export function joinDebug(id: string, hosts: { name: string }[]) {
    let port = 7080
    return `
    <?xml version="1.0" encoding="UTF-8"?>
<ExtensionList>
  <Extension Id="${id}">
    <HostList>
    ${hosts
            .map((host) => `<Host Name="${host.name}" Port="${port++}"/>`)
            .join("\n")}
    </HostList>
  </Extension>
</ExtensionList>
    `
}