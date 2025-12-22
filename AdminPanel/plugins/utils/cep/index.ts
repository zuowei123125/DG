import CSInterface from "./csinterface"

export function initJsx(path: string) {
    console.log('[cep] init jsx', path);
    const cs = new CSInterface()

    cs.evalScript(`$.evalFile("${path}")`, (e) => {
        if (e === 'undefined') return console.log('init json success');
        console.warn('load jsx', e);
    })
}

type JsxTypeof = typeof import('../../../src/jsx/index')
type MethodName = keyof JsxTypeof
export function evalJSX<T extends MethodName>(functionName: T, ...args: Parameters<JsxTypeof[T]>) {
    return new Promise<ReturnType<JsxTypeof[T]>>((resolve, reject) => {
        const formattedArgs = args
            .map((arg) => {
                console.log(JSON.stringify(arg));
                return `${JSON.stringify(arg)}`;
            })
            .join(",");

        const cs = new CSInterface()
        cs.evalScript(
            `try{
              var res = ${functionName}(${formattedArgs});
              JSON.stringify(res)
            }catch(e){
                alert(e);
                e.fileName =new File(e.fileName).fsName;
                JSON.stringify(e)
            }`, (e) => {
            console.log('evalJSX', e);
            if (e === 'undefined') return resolve(null)
            try {
                let parsed = JSON.parse(e);
                if (parsed.name === "ReferenceError") {
                    console.error("REFERENCE ERROR");
                    reject(parsed);
                } else {
                    resolve(parsed);
                }
            } catch (error) {
                reject(error)
            }
        })
    })
}

export function evalFile(path: string) {
    return new Promise((resolve, reject) => {
        const cs = new CSInterface()
        cs.evalScript(`$.evalFile("${path}")`, (e) => {
            if (e === 'undefined') return resolve(null)
            // alert(e)
            console.warn('evalFileError: ' + path, e);
            reject(e)
        })
    })
}

export { CSInterface }
export { CSInterfaceEx } from "./csinterfaceEx"