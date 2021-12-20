from rest_framework.views import APIView
from rest_framework.response import Response


class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def saintelague(self,options,numEscanos):

        for op in options:

            op['postproc'] = 0

        for i in range(0, numEscanos):

            options_copy = []

            for op in options:

                o = op['votes'] / (2*op['postproc']+1)

                options_copy.append(o)

            if op['votes'] != 0:

                maximo = max(options_copy)

                pos_maximo = options_copy.index(maximo)

                options[pos_maximo]['postproc'] += 1
        
        options.sort(key=lambda x: -x['postproc'])

        return Response(options)


    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])
        numEscanyos = request.data.get('numEscanyos', 0)


        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'SAINTELAGUE':
            return self.saintelague(opts,numEscanyos)

        return Response({})
