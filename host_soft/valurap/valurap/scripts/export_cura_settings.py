import configparser
import os
import os.path
import urllib.parse

CURA_CFGS = '~/Library/Application Support/cura/4.5'


def main():
    cfgs = []
    cura_folder = os.path.expanduser(CURA_CFGS)
    for fn, dirs, files in os.walk(cura_folder):
        short_fn = fn[len(cura_folder)+1:]
        if fn == cura_folder:
            if '.git' in dirs:
                dirs.remove('.git')
            if 'cache' in dirs:
                dirs.remove('cache')
        for f in files:
            if f.endswith('.cfg'):
                cfgs.append(os.path.join(short_fn, f))

    data = {}
    used = {}
    machines = {}
    extruders = {}
    settings = {}

    for fn in sorted(cfgs):
        plain_fn = tuple(urllib.parse.unquote(fn).replace('+', " ").split('/'))
        if plain_fn == ("cura.cfg",):
            continue

        cf = configparser.ConfigParser()
        cf.read(os.path.join(cura_folder, fn))
        ok = 1
        if "containers" in cf:
            ok = 1
        if "values" in cf and cf["values"]:
            ok = 1

        if ok:
            if 0:
                print(plain_fn)
                for s in sorted(cf.sections()):
                    print("  ", s)
                    for k in sorted(cf[s].keys()):
                        v = cf[s][k]
                        print("    ", k, v)
            data[plain_fn] = cf
            used[plain_fn] = 0

            ft = cf["metadata"]["type"]
            if ft == 'machine':
                machines[cf["general"]["id"]] = plain_fn
            elif ft == 'extruder_train':
                mach = cf["metadata"]["machine"]
                extruders.setdefault(mach, {})[cf["metadata"]["position"]] = plain_fn
            elif ft in ["definition_changes", "user"]:
                settings[cf["general"]["name"]] = plain_fn
            else:
                raise RuntimeError("Unexpected file type: {}".format(ft))

    for machine in sorted(machines.keys()):
        mf = machines[machine]
        md = data[mf]
        used[mf] = 1
        print("=========== {} ===========".format(md["general"]["name"]))
        for s in ["general", "metadata"]:
            print("  ", s)
            for k in sorted(md[s].keys()):
                v = md[s][k]
                print("    ", k, v)
        extruder_count = 1
        print("   containers:")
        for cn in sorted(md["containers"].keys()):
            cv = md["containers"][cn]
            if cv in settings:
                cf = settings[cv]
                cd = data[cf]
                used[cf] = 1

                print("    ", cn, cv, cf)
                ok = 0
                for k, v in sorted(cd["values"].items()):
                    if '\n' in v:
                        print("        {}:".format(k))
                        for l in v.splitlines():
                            print("          | {}".format(l))

                    else:
                        print("        {}: '{}'".format(k, v))
                    ok = 1
                    if k == "machine_extruder_count":
                        extruder_count = int(v)
                else:
                    if not ok:
                        print("        -- empty --")

            elif cv.startswith("empty_"):
                pass
            elif cv == "normal":
                pass
            elif cv == "custom":
                pass
            elif cv in "extra_fast":
                pass
            else:
                print("    ", cn, cv, 'unknown')
        print("  extruders:")
        for k, ef in sorted(extruders[md["general"]["id"]].items()):
            ed = data[ef]
            used[ef] = 1
            add = (int(k) < extruder_count)
            report = []
            report.append("    {}: --------- {} {} ------- ".format(k, ed["general"]["name"], ef))
            for s in ["general", "metadata"]:
                report.append("        {}".format(s))
                for k in sorted(ed[s].keys()):
                    v = ed[s][k]
                    report.append("          {}: {}".format(k, v))
            report.append("        containers:")
            for cn in sorted(ed["containers"].keys()):
                cv = ed["containers"][cn]
                if cv in settings:
                    cf = settings[cv]
                    cd = data[cf]
                    used[cf] = 1

                    report.append("          {} {} {}".format(cn, cv, cf))
                    ok = 0
                    for k, v in sorted(cd["values"].items()):
                        if '\n' in v:
                            report.append("              {}:".format(k))
                            for l in v.splitlines():
                                report.append("               | {}".format(l))

                        else:
                            report.append("             {}: '{}'".format(k, v))
                        ok = 1
                        add = 1
                    else:
                        if not ok:
                            report.append("             -- empty --")

                elif cv.startswith("generic_"):
                    pass
                elif cv.startswith("empty_"):
                    pass
                elif cv.startswith("custom_extruder_"):
                    pass
                elif cv == "normal":
                    pass
                elif cv == "extra_fast":
                    pass
                else:
                    report.append("          {} {} unknown".format(cn, cv))
            if add:
                print("\n".join(report))



    for k, v in used.items():
        if not v:
            print("Not used:", k)





if __name__ == "__main__":
    main()
