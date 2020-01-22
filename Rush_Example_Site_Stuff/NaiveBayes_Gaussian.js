var GaussianNB = function(priors, sigmas, thetas) {

    this.priors = priors;
    this.sigmas = sigmas;
    this.thetas = thetas;

    this.predict = function(features) {
        var likelihoods = new Array(this.sigmas.length);
    
        for (var i = 0, il = this.sigmas.length; i < il; i++) {
            var sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.log(2. * Math.PI * this.sigmas[i][j]);
            }
            var nij = -0.5 * sum;
            sum = 0.;
            for (var j = 0, jl = this.sigmas[0].length; j < jl; j++) {
                sum += Math.pow(features[j] - this.thetas[i][j], 2.) / this.sigmas[i][j];
            }
            nij -= 0.5 * sum;
            likelihoods[i] = Math.log(this.priors[i]) + nij;
        }
    
        var classIdx = 0;
        for (var i = 0, l = likelihoods.length; i < l; i++) {
            classIdx = likelihoods[i] > likelihoods[classIdx] ? i : classIdx;
        }
        return classIdx;
    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        var priors = [0.499574358974359, 0.500425641025641];
        var sigmas = [[325477746.5801683, 44719024.745114736, 15.397794047610583, 13942.172251175227, 1845.930163039415, 4.773956450685417, 0.44157080989097064, 0.4089454328003829], [18858696.75565271, 392257.6492173077, 0.19340899093500433, 4.303474429219202, 181935524.11162433, 0.6317605919903297, 0.35464204395795607, 0.9507778244826861]];
        var thetas = [[10839.319718324317, 5163.905950706756, 0.3815555806481415, 7.4244946980506485, 2.6733937608425635, 1.0734676699138754, 0.33085601075787596, 0.31003828900499913], [1593.500210077575, 753.8926349876515, 0.0, 0.44086572456268, 595.336861953414, 0.24338255638789544, 0.19248229712142484, 0.8425647909984321]];

        // Estimator:
        var clf = new GaussianNB(priors, sigmas, thetas);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}